package com.house.adminservice.repository;

import com.house.common.entity.House;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface HouseRepository extends JpaRepository<House, Long> {
    
    Optional<House> findByZillowId(String zillowId);
}
