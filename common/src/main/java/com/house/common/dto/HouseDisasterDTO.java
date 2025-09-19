package com.house.common.dto;

import jakarta.validation.constraints.NotNull;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class HouseDisasterDTO {

    private Long id;

    @NotNull
    private Long houseId;

    @NotNull
    private String disasterType;

    @NotNull
    private LocalDate disasterDate;

    private String description;

    private String severity;

    private LocalDateTime createdAt;

    // Constructors
    public HouseDisasterDTO() {
    }

    public HouseDisasterDTO(Long houseId, String disasterType, LocalDate disasterDate) {
        this.houseId = houseId;
        this.disasterType = disasterType;
        this.disasterDate = disasterDate;
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

    public String getDisasterType() {
        return disasterType;
    }

    public void setDisasterType(String disasterType) {
        this.disasterType = disasterType;
    }

    public LocalDate getDisasterDate() {
        return disasterDate;
    }

    public void setDisasterDate(LocalDate disasterDate) {
        this.disasterDate = disasterDate;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
