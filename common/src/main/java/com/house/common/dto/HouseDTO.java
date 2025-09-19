package com.house.common.dto;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

public class HouseDTO {

    private Long id;

    @NotBlank
    private String address;

    @NotBlank
    private String city;

    @NotBlank
    private String state;

    @NotBlank
    private String zipCode;

    @NotNull
    @DecimalMin(value = "-90.0")
    @DecimalMax(value = "90.0")
    private BigDecimal latitude;

    @NotNull
    @DecimalMin(value = "-180.0")
    @DecimalMax(value = "180.0")
    private BigDecimal longitude;

    @NotNull
    private String houseType;

    @NotNull
    private Integer areaSqft;

    private Integer lotAreaSqft;

    @NotNull
    private String houseStatus;

    private Integer buildYear;

    private Integer bathrooms = 0;

    private Integer bedrooms = 0;

    private String description;

    private String zillowId;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    private List<HouseSaleDTO> sales;

    private List<HouseMaintenanceDTO> maintenanceRecords;

    private List<HouseDisasterDTO> disasters;

    // Constructors
    public HouseDTO() {
    }

    public HouseDTO(String address, String city, String state, String zipCode,
            BigDecimal latitude, BigDecimal longitude, String houseType,
            Integer areaSqft, String houseStatus) {
        this.address = address;
        this.city = city;
        this.state = state;
        this.zipCode = zipCode;
        this.latitude = latitude;
        this.longitude = longitude;
        this.houseType = houseType;
        this.areaSqft = areaSqft;
        this.houseStatus = houseStatus;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getZipCode() {
        return zipCode;
    }

    public void setZipCode(String zipCode) {
        this.zipCode = zipCode;
    }

    public BigDecimal getLatitude() {
        return latitude;
    }

    public void setLatitude(BigDecimal latitude) {
        this.latitude = latitude;
    }

    public BigDecimal getLongitude() {
        return longitude;
    }

    public void setLongitude(BigDecimal longitude) {
        this.longitude = longitude;
    }

    public String getHouseType() {
        return houseType;
    }

    public void setHouseType(String houseType) {
        this.houseType = houseType;
    }

    public Integer getAreaSqft() {
        return areaSqft;
    }

    public void setAreaSqft(Integer areaSqft) {
        this.areaSqft = areaSqft;
    }

    public Integer getLotAreaSqft() {
        return lotAreaSqft;
    }

    public void setLotAreaSqft(Integer lotAreaSqft) {
        this.lotAreaSqft = lotAreaSqft;
    }

    public String getHouseStatus() {
        return houseStatus;
    }

    public void setHouseStatus(String houseStatus) {
        this.houseStatus = houseStatus;
    }

    public Integer getBuildYear() {
        return buildYear;
    }

    public void setBuildYear(Integer buildYear) {
        this.buildYear = buildYear;
    }

    public Integer getBathrooms() {
        return bathrooms;
    }

    public void setBathrooms(Integer bathrooms) {
        this.bathrooms = bathrooms;
    }

    public Integer getBedrooms() {
        return bedrooms;
    }

    public void setBedrooms(Integer bedrooms) {
        this.bedrooms = bedrooms;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getZillowId() {
        return zillowId;
    }

    public void setZillowId(String zillowId) {
        this.zillowId = zillowId;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    public List<HouseSaleDTO> getSales() {
        return sales;
    }

    public void setSales(List<HouseSaleDTO> sales) {
        this.sales = sales;
    }

    public List<HouseMaintenanceDTO> getMaintenanceRecords() {
        return maintenanceRecords;
    }

    public void setMaintenanceRecords(List<HouseMaintenanceDTO> maintenanceRecords) {
        this.maintenanceRecords = maintenanceRecords;
    }

    public List<HouseDisasterDTO> getDisasters() {
        return disasters;
    }

    public void setDisasters(List<HouseDisasterDTO> disasters) {
        this.disasters = disasters;
    }
}
