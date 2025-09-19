package com.house.common.dto;

import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class HouseSaleDTO {

    private Long id;

    @NotNull
    private Long houseId;

    @NotNull
    private LocalDate saleDate;

    @NotNull
    private BigDecimal salePrice;

    private String buyerName;

    private String sellerName;

    private LocalDateTime createdAt;

    // Constructors
    public HouseSaleDTO() {
    }

    public HouseSaleDTO(Long houseId, LocalDate saleDate, BigDecimal salePrice) {
        this.houseId = houseId;
        this.saleDate = saleDate;
        this.salePrice = salePrice;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getHouseId() {
        return houseId;
    }

    public void setHouseId(Long houseId) {
        this.houseId = houseId;
    }

    public LocalDate getSaleDate() {
        return saleDate;
    }

    public void setSaleDate(LocalDate saleDate) {
        this.saleDate = saleDate;
    }

    public BigDecimal getSalePrice() {
        return salePrice;
    }

    public void setSalePrice(BigDecimal salePrice) {
        this.salePrice = salePrice;
    }

    public String getBuyerName() {
        return buyerName;
    }

    public void setBuyerName(String buyerName) {
        this.buyerName = buyerName;
    }

    public String getSellerName() {
        return sellerName;
    }

    public void setSellerName(String sellerName) {
        this.sellerName = sellerName;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
