package com.house.common.dto;

import java.math.BigDecimal;

public class GeospatialSearchResult {

    private HouseDTO house;

    private Double distanceKm;

    private BigDecimal distanceMeters;

    // Constructors
    public GeospatialSearchResult() {
    }

    public GeospatialSearchResult(HouseDTO house, Double distanceKm) {
        this.house = house;
        this.distanceKm = distanceKm;
        this.distanceMeters = BigDecimal.valueOf(distanceKm * 1000);
    }

    // Getters and Setters
    public HouseDTO getHouse() {
        return house;
    }

    public void setHouse(HouseDTO house) {
        this.house = house;
    }

    public Double getDistanceKm() {
        return distanceKm;
    }

    public void setDistanceKm(Double distanceKm) {
        this.distanceKm = distanceKm;
        this.distanceMeters = BigDecimal.valueOf(distanceKm * 1000);
    }

    public BigDecimal getDistanceMeters() {
        return distanceMeters;
    }

    public void setDistanceMeters(BigDecimal distanceMeters) {
        this.distanceMeters = distanceMeters;
    }
}
