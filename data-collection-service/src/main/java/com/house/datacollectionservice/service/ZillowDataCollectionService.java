package com.house.datacollectionservice.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.house.datacollectionservice.model.ZillowProperty;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;

@Service
public class ZillowDataCollectionService {
    
    @Autowired
    private WebClient.Builder webClientBuilder;
    
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Value("${zillow.api.key}")
    private String zillowApiKey;
    
    @Value("${zillow.api.base-url}")
    private String zillowBaseUrl;
    
    @Value("${rabbitmq.queue.zillow-data}")
    private String zillowDataQueue;
    
    // 定时任务：每天凌晨2点执行数据采集
    @Scheduled(cron = "0 0 2 * * ?")
    public void collectZillowData() {
        System.out.println("Starting Zillow data collection...");
        
        // 这里可以配置多个城市进行数据采集
        String[] cities = {"San Francisco", "New York", "Los Angeles", "Chicago", "Seattle"};
        
        for (String city : cities) {
            try {
                List<ZillowProperty> properties = fetchPropertiesFromZillow(city);
                sendToQueue(properties);
                Thread.sleep(1000); // 避免API调用过于频繁
            } catch (Exception e) {
                System.err.println("Error collecting data for city " + city + ": " + e.getMessage());
            }
        }
        
        System.out.println("Zillow data collection completed.");
    }
    
    public List<ZillowProperty> fetchPropertiesFromZillow(String city) {
        try {
            WebClient webClient = webClientBuilder.build();
            
            // 构建Zillow API请求
            String url = zillowBaseUrl + "/GetSearchResults.htm?" +
                        "zws-id=" + zillowApiKey +
                        "&address=" + city +
                        "&citystatezip=" + city;
            
            Mono<String> response = webClient.get()
                    .uri(url)
                    .retrieve()
                    .bodyToMono(String.class);
            
            String responseBody = response.block();
            return parseZillowResponse(responseBody);
            
        } catch (Exception e) {
            System.err.println("Error fetching data from Zillow: " + e.getMessage());
            return new ArrayList<>();
        }
    }
    
    private List<ZillowProperty> parseZillowResponse(String response) {
        List<ZillowProperty> properties = new ArrayList<>();
        
        try {
            JsonNode rootNode = objectMapper.readTree(response);
            JsonNode searchResults = rootNode.path("SearchResults").path("results");
            
            if (searchResults.isArray()) {
                for (JsonNode propertyNode : searchResults) {
                    ZillowProperty property = parsePropertyNode(propertyNode);
                    if (property != null) {
                        properties.add(property);
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Error parsing Zillow response: " + e.getMessage());
        }
        
        return properties;
    }
    
    private ZillowProperty parsePropertyNode(JsonNode propertyNode) {
        try {
            ZillowProperty property = new ZillowProperty();
            
            property.setZpid(propertyNode.path("zpid").asText());
            property.setStreetAddress(propertyNode.path("address").path("street").asText());
            property.setCity(propertyNode.path("address").path("city").asText());
            property.setState(propertyNode.path("address").path("state").asText());
            property.setZipcode(propertyNode.path("address").path("zipcode").asText());
            
            // 解析坐标
            JsonNode coordinates = propertyNode.path("address").path("latitudeLongitude");
            if (!coordinates.isMissingNode()) {
                property.setLatitude(coordinates.path("latitude").decimalValue());
                property.setLongitude(coordinates.path("longitude").decimalValue());
            }
            
            // 解析房屋信息
            JsonNode zestimate = propertyNode.path("zestimate");
            if (!zestimate.isMissingNode()) {
                property.setPrice(zestimate.path("amount").asInt());
            }
            
            JsonNode useCode = propertyNode.path("useCode");
            property.setHomeType(useCode.asText());
            
            // 解析详细信息
            JsonNode details = propertyNode.path("editedFacts");
            if (!details.isMissingNode()) {
                property.setBedrooms(details.path("bedrooms").asInt());
                property.setBathrooms(details.path("bathrooms").decimalValue());
                property.setLivingArea(details.path("finishedSqFt").asInt());
                property.setLotAreaValue(details.path("lotSizeSqFt").asInt());
                property.setYearBuilt(details.path("yearBuilt").asInt());
            }
            
            // 解析状态
            property.setHomeStatus(propertyNode.path("homeStatus").asText());
            
            return property;
            
        } catch (Exception e) {
            System.err.println("Error parsing property node: " + e.getMessage());
            return null;
        }
    }
    
    private void sendToQueue(List<ZillowProperty> properties) {
        for (ZillowProperty property : properties) {
            try {
                rabbitTemplate.convertAndSend(zillowDataQueue, property);
                System.out.println("Sent property to queue: " + property.getZpid());
            } catch (Exception e) {
                System.err.println("Error sending property to queue: " + e.getMessage());
            }
        }
    }
    
    // 手动触发数据采集的API端点
    public void triggerDataCollection() {
        new Thread(this::collectZillowData).start();
    }
}
