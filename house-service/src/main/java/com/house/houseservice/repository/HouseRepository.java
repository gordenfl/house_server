package com.house.houseservice.repository;

import com.house.common.entity.House;
import com.house.common.entity.HouseStatus;
import com.house.common.entity.HouseType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@Repository
public interface HouseRepository extends JpaRepository<House, Long> {
    
    List<House> findByCityAndState(String city, String state);
    
    List<House> findByHouseStatus(HouseStatus houseStatus);
    
    List<House> findByHouseType(HouseType houseType);
    
    Optional<House> findByZillowId(String zillowId);
    
    @Query("SELECT h FROM House h WHERE h.latitude BETWEEN :minLat AND :maxLat AND h.longitude BETWEEN :minLng AND :maxLng")
    List<House> findByLocationRange(@Param("minLat") BigDecimal minLat, 
                                   @Param("maxLat") BigDecimal maxLat,
                                   @Param("minLng") BigDecimal minLng, 
                                   @Param("maxLng") BigDecimal maxLng);
    
    @Query("SELECT h FROM House h WHERE " +
           "6371 * acos(cos(radians(:lat)) * cos(radians(h.latitude)) * " +
           "cos(radians(h.longitude) - radians(:lng)) + sin(radians(:lat)) * " +
           "sin(radians(h.latitude))) <= :radiusKm")
    List<House> findByLocationWithinRadius(@Param("lat") BigDecimal latitude,
                                          @Param("lng") BigDecimal longitude,
                                          @Param("radiusKm") Double radiusKm);
    
    @Query("SELECT h FROM House h WHERE h.houseStatus.name = :status")
    List<House> findByHouseStatusName(@Param("status") String status);
    
    @Query("SELECT h FROM House h WHERE h.houseType.name = :type")
    List<House> findByHouseTypeName(@Param("type") String type);
}
