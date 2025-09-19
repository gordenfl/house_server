package com.house.houseservice.service;

import com.house.common.dto.GeospatialSearchRequest;
import com.house.common.dto.GeospatialSearchResult;
import com.house.common.dto.HouseDTO;
import com.house.common.entity.*;
import com.house.houseservice.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

@Service
@Transactional
public class HouseService {
    
    @Autowired
    private HouseRepository houseRepository;
    
    @Autowired
    private HouseTypeRepository houseTypeRepository;
    
    @Autowired
    private HouseStatusRepository houseStatusRepository;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    private static final String HOUSE_CACHE_PREFIX = "house:";
    private static final long CACHE_TTL_MINUTES = 30;
    
    public HouseDTO createHouse(HouseDTO houseDTO) {
        HouseType houseType = houseTypeRepository.findByName(houseDTO.getHouseType())
                .orElseThrow(() -> new RuntimeException("House type not found: " + houseDTO.getHouseType()));
        
        HouseStatus houseStatus = houseStatusRepository.findByName(houseDTO.getHouseStatus())
                .orElseThrow(() -> new RuntimeException("House status not found: " + houseDTO.getHouseStatus()));
        
        House house = new House();
        house.setAddress(houseDTO.getAddress());
        house.setCity(houseDTO.getCity());
        house.setState(houseDTO.getState());
        house.setZipCode(houseDTO.getZipCode());
        house.setLatitude(houseDTO.getLatitude());
        house.setLongitude(houseDTO.getLongitude());
        house.setHouseType(houseType);
        house.setAreaSqft(houseDTO.getAreaSqft());
        house.setLotAreaSqft(houseDTO.getLotAreaSqft());
        house.setHouseStatus(houseStatus);
        house.setBuildYear(houseDTO.getBuildYear());
        house.setBathrooms(houseDTO.getBathrooms());
        house.setBedrooms(houseDTO.getBedrooms());
        house.setDescription(houseDTO.getDescription());
        house.setZillowId(houseDTO.getZillowId());
        
        House savedHouse = houseRepository.save(house);
        
        // Cache the house
        cacheHouse(savedHouse);
        
        return convertToDTO(savedHouse);
    }
    
    public Optional<HouseDTO> getHouseById(Long id) {
        // Try to get from cache first
        String cacheKey = HOUSE_CACHE_PREFIX + id;
        House cachedHouse = (House) redisTemplate.opsForValue().get(cacheKey);
        
        if (cachedHouse != null) {
            return Optional.of(convertToDTO(cachedHouse));
        }
        
        // Get from database
        Optional<House> houseOpt = houseRepository.findById(id);
        if (houseOpt.isPresent()) {
            House house = houseOpt.get();
            cacheHouse(house);
            return Optional.of(convertToDTO(house));
        }
        
        return Optional.empty();
    }
    
    public List<HouseDTO> getAllHouses() {
        return houseRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public List<HouseDTO> getHousesByCityAndState(String city, String state) {
        return houseRepository.findByCityAndState(city, state).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public List<HouseDTO> getHousesByStatus(String status) {
        return houseRepository.findByHouseStatusName(status).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public List<HouseDTO> getHousesByType(String type) {
        return houseRepository.findByHouseTypeName(type).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public List<GeospatialSearchResult> searchHousesByLocation(GeospatialSearchRequest request) {
        List<House> houses = houseRepository.findByLocationWithinRadius(
                request.getLatitude(),
                request.getLongitude(),
                request.getRadiusKm()
        );
        
        return houses.stream()
                .map(house -> {
                    double distance = calculateDistance(
                            request.getLatitude().doubleValue(),
                            request.getLongitude().doubleValue(),
                            house.getLatitude().doubleValue(),
                            house.getLongitude().doubleValue()
                    );
                    return new GeospatialSearchResult(convertToDTO(house), distance);
                })
                .collect(Collectors.toList());
    }
    
    public HouseDTO updateHouse(Long id, HouseDTO houseDTO) {
        House house = houseRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("House not found"));
        
        // Update fields
        house.setAddress(houseDTO.getAddress());
        house.setCity(houseDTO.getCity());
        house.setState(houseDTO.getState());
        house.setZipCode(houseDTO.getZipCode());
        house.setLatitude(houseDTO.getLatitude());
        house.setLongitude(houseDTO.getLongitude());
        house.setAreaSqft(houseDTO.getAreaSqft());
        house.setLotAreaSqft(houseDTO.getLotAreaSqft());
        house.setBuildYear(houseDTO.getBuildYear());
        house.setBathrooms(houseDTO.getBathrooms());
        house.setBedrooms(houseDTO.getBedrooms());
        house.setDescription(houseDTO.getDescription());
        house.setZillowId(houseDTO.getZillowId());
        
        // Update type and status if provided
        if (houseDTO.getHouseType() != null) {
            HouseType houseType = houseTypeRepository.findByName(houseDTO.getHouseType())
                    .orElseThrow(() -> new RuntimeException("House type not found: " + houseDTO.getHouseType()));
            house.setHouseType(houseType);
        }
        
        if (houseDTO.getHouseStatus() != null) {
            HouseStatus houseStatus = houseStatusRepository.findByName(houseDTO.getHouseStatus())
                    .orElseThrow(() -> new RuntimeException("House status not found: " + houseDTO.getHouseStatus()));
            house.setHouseStatus(houseStatus);
        }
        
        House savedHouse = houseRepository.save(house);
        
        // Update cache
        cacheHouse(savedHouse);
        
        return convertToDTO(savedHouse);
    }
    
    public void deleteHouse(Long id) {
        if (!houseRepository.existsById(id)) {
            throw new RuntimeException("House not found");
        }
        
        houseRepository.deleteById(id);
        
        // Remove from cache
        String cacheKey = HOUSE_CACHE_PREFIX + id;
        redisTemplate.delete(cacheKey);
    }
    
    public Optional<HouseDTO> getHouseByZillowId(String zillowId) {
        return houseRepository.findByZillowId(zillowId).map(this::convertToDTO);
    }
    
    private void cacheHouse(House house) {
        String cacheKey = HOUSE_CACHE_PREFIX + house.getId();
        redisTemplate.opsForValue().set(cacheKey, house, CACHE_TTL_MINUTES, TimeUnit.MINUTES);
    }
    
    private double calculateDistance(double lat1, double lon1, double lat2, double lon2) {
        final int R = 6371; // Radius of the earth in km
        double latDistance = Math.toRadians(lat2 - lat1);
        double lonDistance = Math.toRadians(lon2 - lon1);
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2))
                * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c; // Distance in km
    }
    
    private HouseDTO convertToDTO(House house) {
        HouseDTO dto = new HouseDTO();
        dto.setId(house.getId());
        dto.setAddress(house.getAddress());
        dto.setCity(house.getCity());
        dto.setState(house.getState());
        dto.setZipCode(house.getZipCode());
        dto.setLatitude(house.getLatitude());
        dto.setLongitude(house.getLongitude());
        dto.setHouseType(house.getHouseType().getName());
        dto.setAreaSqft(house.getAreaSqft());
        dto.setLotAreaSqft(house.getLotAreaSqft());
        dto.setHouseStatus(house.getHouseStatus().getName());
        dto.setBuildYear(house.getBuildYear());
        dto.setBathrooms(house.getBathrooms());
        dto.setBedrooms(house.getBedrooms());
        dto.setDescription(house.getDescription());
        dto.setZillowId(house.getZillowId());
        dto.setCreatedAt(house.getCreatedAt());
        dto.setUpdatedAt(house.getUpdatedAt());
        
        // Convert related entities
        if (house.getSales() != null) {
            dto.setSales(house.getSales().stream()
                    .map(this::convertSaleToDTO)
                    .collect(Collectors.toList()));
        }
        
        if (house.getMaintenanceRecords() != null) {
            dto.setMaintenanceRecords(house.getMaintenanceRecords().stream()
                    .map(this::convertMaintenanceToDTO)
                    .collect(Collectors.toList()));
        }
        
        if (house.getDisasters() != null) {
            dto.setDisasters(house.getDisasters().stream()
                    .map(this::convertDisasterToDTO)
                    .collect(Collectors.toList()));
        }
        
        return dto;
    }
    
    private com.house.common.dto.HouseSaleDTO convertSaleToDTO(HouseSale sale) {
        com.house.common.dto.HouseSaleDTO dto = new com.house.common.dto.HouseSaleDTO();
        dto.setId(sale.getId());
        dto.setHouseId(sale.getHouse().getId());
        dto.setSaleDate(sale.getSaleDate());
        dto.setSalePrice(sale.getSalePrice());
        dto.setBuyerName(sale.getBuyerName());
        dto.setSellerName(sale.getSellerName());
        dto.setCreatedAt(sale.getCreatedAt());
        return dto;
    }
    
    private com.house.common.dto.HouseMaintenanceDTO convertMaintenanceToDTO(HouseMaintenance maintenance) {
        com.house.common.dto.HouseMaintenanceDTO dto = new com.house.common.dto.HouseMaintenanceDTO();
        dto.setId(maintenance.getId());
        dto.setHouseId(maintenance.getHouse().getId());
        dto.setMaintenanceDate(maintenance.getMaintenanceDate());
        dto.setMaintenanceScale(maintenance.getMaintenanceScale().getName());
        dto.setCost(maintenance.getCost());
        dto.setDescription(maintenance.getDescription());
        dto.setContractorName(maintenance.getContractorName());
        dto.setCreatedAt(maintenance.getCreatedAt());
        return dto;
    }
    
    private com.house.common.dto.HouseDisasterDTO convertDisasterToDTO(HouseDisaster disaster) {
        com.house.common.dto.HouseDisasterDTO dto = new com.house.common.dto.HouseDisasterDTO();
        dto.setId(disaster.getId());
        dto.setHouseId(disaster.getHouse().getId());
        dto.setDisasterType(disaster.getDisasterType().getName());
        dto.setDisasterDate(disaster.getDisasterDate());
        dto.setDescription(disaster.getDescription());
        dto.setSeverity(disaster.getSeverity().name());
        dto.setCreatedAt(disaster.getCreatedAt());
        return dto;
    }
}
