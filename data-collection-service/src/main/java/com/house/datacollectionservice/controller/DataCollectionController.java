package com.house.datacollectionservice.controller;

import com.house.datacollectionservice.service.ZillowDataCollectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/data-collection")
@CrossOrigin(origins = "*")
public class DataCollectionController {
    
    @Autowired
    private ZillowDataCollectionService zillowDataCollectionService;
    
    @PostMapping("/trigger")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> triggerDataCollection() {
        try {
            zillowDataCollectionService.triggerDataCollection();
            return ResponseEntity.ok(Map.of("message", "Data collection triggered successfully"));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/status")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> getCollectionStatus() {
        // 这里可以返回数据采集的状态信息
        return ResponseEntity.ok(Map.of("status", "active", "lastRun", "2024-01-01T02:00:00Z"));
    }
}
