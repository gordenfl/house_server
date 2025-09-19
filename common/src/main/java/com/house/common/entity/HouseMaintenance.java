package com.house.common.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "house_maintenance")
@EntityListeners(AuditingEntityListener.class)
public class HouseMaintenance {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "house_id", nullable = false)
    private House house;

    @NotNull
    private LocalDate maintenanceDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "maintenance_scale_id", nullable = false)
    private MaintenanceScale maintenanceScale;

    @NotNull
    private BigDecimal cost;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String contractorName;

    @CreatedDate
    private LocalDateTime createdAt;

    // Constructors
    public HouseMaintenance() {
    }

    public HouseMaintenance(House house, LocalDate maintenanceDate, MaintenanceScale maintenanceScale,
            BigDecimal cost) {
        this.house = house;
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

    public House getHouse() {
        return house;
    }

    public void setHouse(House house) {
        this.house = house;
    }

    public LocalDate getMaintenanceDate() {
        return maintenanceDate;
    }

    public void setMaintenanceDate(LocalDate maintenanceDate) {
        this.maintenanceDate = maintenanceDate;
    }

    public MaintenanceScale getMaintenanceScale() {
        return maintenanceScale;
    }

    public void setMaintenanceScale(MaintenanceScale maintenanceScale) {
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
