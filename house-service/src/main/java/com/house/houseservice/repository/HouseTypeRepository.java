package com.house.houseservice.repository;

import com.house.common.entity.HouseType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface HouseTypeRepository extends JpaRepository<HouseType, Integer> {
    
    Optional<HouseType> findByName(String name);
}
