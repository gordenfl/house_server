package com.house.datacollectionservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableEurekaClient
@EnableScheduling
public class DataCollectionServiceApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(DataCollectionServiceApplication.class, args);
    }
}
