package com.olx.scraper.models

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.google.gson.annotations.SerializedName

@Entity(tableName = "olx_items")
data class OLXItem(
    @PrimaryKey
    val id: String,
    val title: String,
    val description: String? = null,
    val category: String,
    val price: Double? = null,
    val location: String? = null,
    @SerializedName("seller_name")
    val sellerName: String? = null,
    @SerializedName("seller_rating")
    val sellerRating: Double? = null,
    val url: String? = null,
    @SerializedName("image_url")
    val imageUrl: String? = null,
    @SerializedName("discovered_at")
    val discoveredAt: String? = null,
    @SerializedName("notification_sent")
    val notificationSent: Boolean = false,
    val isFavorite: Boolean = false,
    val savedAt: Long = System.currentTimeMillis()
)
