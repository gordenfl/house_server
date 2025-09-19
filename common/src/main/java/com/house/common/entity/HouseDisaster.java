package com.house.common.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "house_disasters")
@EntityListeners(AuditingEntityListener.class)
public class HouseDisaster {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "house_id", nullable = false)
    private House house;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "disaster_type_id", nullable = false)
    private DisasterType disasterType;

    @NotNull
    private LocalDate disasterDate;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Enumerated(EnumType.STRING)
    private Severity severity = Severity.MEDIUM;

    @CreatedDate
    private LocalDateTime createdAt;

    public enum Severity {
        LOW, MEDIUM, HIGH, CRITICAL
    }

    // Constructors
    public HouseDisaster() {
    }

    public HouseDisaster(House house, DisasterType disasterType, LocalDate disasterDate) {
        this.house = house;
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

    public House getHouse() {
        return house;
    }

    public void setHouse(House house) {
        this.house = house;
    }

    public DisasterType getDisasterType() {
        return disasterType;
    }

    public void setDisasterType(DisasterType disasterType) {
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

    public Severity getSeverity() {
        return severity;
    }

    public void setSeverity(Severity severity) {
        this.severity = severity;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
