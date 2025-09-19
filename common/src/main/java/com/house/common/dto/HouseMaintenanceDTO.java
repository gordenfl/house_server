package com.house.common.dto;

import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class HouseMaintenanceDTO {

    private Long id;

    @NotNull
    private Long houseId;

    @NotNull
    private LocalDate maintenanceDate;

    @NotNull
    private String maintenanceScale;

    @NotNull
    private BigDecimal cost;

    private String description;

    private String contractorName;

    private LocalDateTime createdAt;

    // Constructors
    public HouseMaintenanceDTO() {
    }

    public HouseMaintenanceDTO(Long houseId, LocalDate maintenanceDate, String maintenanceScale, BigDecimal cost) {
        this.houseId = houseId;
        this.maintenanceDate = maintenanceDate;
        this.maintenanceScale = maintenanceScale;
        this.cost = cost;
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

    public LocalDate getMaintenanceDate() {
        return maintenanceDate;
    }

    public void setMaintenanceDate(LocalDate maintenanceDate) {
        this.maintenanceDate = maintenanceDate;
    }

    public String getMaintenanceScale() {
        return maintenanceScale;
    }

    public void setMaintenanceScale(String maintenanceScale) {
        this.maintenanceScale = maintenanceScale;
    }

    public BigDecimal getCost() {
        return cost;
    }

    public void setCost(BigDecimal cost) {
        this.cost = cost;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getContractorName() {
        return contractorName;
    }

    public void setContractorName(String contractorName) {
        this.contractorName = contractorName;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
