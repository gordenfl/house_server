package com.house.houseservice.controller;

import com.house.common.dto.GeospatialSearchRequest;
import com.house.common.dto.GeospatialSearchResult;
import com.house.common.dto.HouseDTO;
import com.house.houseservice.service.HouseService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/houses")
@CrossOrigin(origins = "*")
public class HouseController {
    
    @Autowired
    private HouseService houseService;
    
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> createHouse(@Valid @RequestBody HouseDTO houseDTO) {
        try {
            HouseDTO createdHouse = houseService.createHouse(houseDTO);
            return ResponseEntity.status(HttpStatus.CREATED).body(createdHouse);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<?> getHouseById(@PathVariable Long id) {
        Optional<HouseDTO> house = houseService.getHouseById(id);
        if (house.isPresent()) {
            return ResponseEntity.ok(house.get());
        }
        return ResponseEntity.notFound().build();
    }
    
    @GetMapping
    public ResponseEntity<List<HouseDTO>> getAllHouses(
            @RequestParam(required = false) String city,
            @RequestParam(required = false) String state,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String type) {
        
        List<HouseDTO> houses;
        
        if (city != null && state != null) {
            houses = houseService.getHousesByCityAndState(city, state);
        } else if (status != null) {
            houses = houseService.getHousesByStatus(status);
        } else if (type != null) {
            houses = houseService.getHousesByType(type);
        } else {
            houses = houseService.getAllHouses();
        }
        
        return ResponseEntity.ok(houses);
    }
    
    @PostMapping("/search/location")
    public ResponseEntity<?> searchHousesByLocation(@Valid @RequestBody GeospatialSearchRequest request) {
        try {
            List<GeospatialSearchResult> results = houseService.searchHousesByLocation(request);
            return ResponseEntity.ok(results);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/zillow/{zillowId}")
    public ResponseEntity<?> getHouseByZillowId(@PathVariable String zillowId) {
        Optional<HouseDTO> house = houseService.getHouseByZillowId(zillowId);
        if (house.isPresent()) {
            return ResponseEntity.ok(house.get());
        }
        return ResponseEntity.notFound().build();
    }
    
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> updateHouse(@PathVariable Long id, @Valid @RequestBody HouseDTO houseDTO) {
        try {
            HouseDTO updatedHouse = houseService.updateHouse(id, houseDTO);
            return ResponseEntity.ok(updatedHouse);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> deleteHouse(@PathVariable Long id) {
        try {
            houseService.deleteHouse(id);
            return ResponseEntity.ok(Map.of("message", "House deleted successfully"));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
