package com.house.houseservice.repository;

import com.house.common.entity.HouseStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface HouseStatusRepository extends JpaRepository<HouseStatus, Integer> {
    
    Optional<HouseStatus> findByName(String name);
}
