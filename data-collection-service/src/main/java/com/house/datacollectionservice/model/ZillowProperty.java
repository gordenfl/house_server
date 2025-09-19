package com.house.datacollectionservice.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;

public class ZillowProperty {
    
    @JsonProperty("zpid")
    private String zpid;
    
    @JsonProperty("streetAddress")
    private String streetAddress;
    
    @JsonProperty("city")
    private String city;
    
    @JsonProperty("state")
    private String state;
    
    @JsonProperty("zipcode")
    private String zipcode;
    
    @JsonProperty("latitude")
    private BigDecimal latitude;
    
    @JsonProperty("longitude")
    private BigDecimal longitude;
    
    @JsonProperty("homeType")
    private String homeType;
    
    @JsonProperty("price")
    private Integer price;
    
    @JsonProperty("bathrooms")
    private BigDecimal bathrooms;
    
    @JsonProperty("bedrooms")
    private Integer bedrooms;
    
    @JsonProperty("livingArea")
    private Integer livingArea;
    
    @JsonProperty("lotAreaValue")
    private Integer lotAreaValue;
    
    @JsonProperty("yearBuilt")
    private Integer yearBuilt;
    
    @JsonProperty("homeStatus")
    private String homeStatus;
    
    @JsonProperty("description")
    private String description;
    
    // Constructors
    public ZillowProperty() {}
    
    // Getters and Setters
    public String getZpid() { return zpid; }
    public void setZpid(String zpid) { this.zpid = zpid; }
    
    public String getStreetAddress() { return streetAddress; }
    public void setStreetAddress(String streetAddress) { this.streetAddress = streetAddress; }
    
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
    
    public String getState() { return state; }
    public void setState(String state) { this.state = state; }
    
    public String getZipcode() { return zipcode; }
    public void setZipcode(String zipcode) { this.zipcode = zipcode; }
    
    public BigDecimal getLatitude() { return latitude; }
    public void setLatitude(BigDecimal latitude) { this.latitude = latitude; }
    
    public BigDecimal getLongitude() { return longitude; }
    public void setLongitude(BigDecimal longitude) { this.longitude = longitude; }
    
    public String getHomeType() { return homeType; }
    public void setHomeType(String homeType) { this.homeType = homeType; }
    
    public Integer getPrice() { return price; }
    public void setPrice(Integer price) { this.price = price; }
    
    public BigDecimal getBathrooms() { return bathrooms; }
    public void setBathrooms(BigDecimal bathrooms) { this.bathrooms = bathrooms; }
    
    public Integer getBedrooms() { return bedrooms; }
    public void setBedrooms(Integer bedrooms) { this.bedrooms = bedrooms; }
    
    public Integer getLivingArea() { return livingArea; }
    public void setLivingArea(Integer livingArea) { this.livingArea = livingArea; }
    
    public Integer getLotAreaValue() { return lotAreaValue; }
    public void setLotAreaValue(Integer lotAreaValue) { this.lotAreaValue = lotAreaValue; }
    
    public Integer getYearBuilt() { return yearBuilt; }
    public void setYearBuilt(Integer yearBuilt) { this.yearBuilt = yearBuilt; }
    
    public String getHomeStatus() { return homeStatus; }
    public void setHomeStatus(String homeStatus) { this.homeStatus = homeStatus; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
