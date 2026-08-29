package com.olx.scraper.api

import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface ApiService {
    @GET("api/listings")
    fun getListings(): Call<ListingsResponse>

    @GET("api/listings/{id}")
    fun getListing(@Path("id") id: Int): Call<ListingResponse>

    @GET("api/search")
    fun search(@Query("q") query: String): Call<SearchResponse>

    @GET("api/health")
    fun health(): Call<HealthResponse>
}

data class ListingsResponse(
    val status: String,
    val data: List<Listing>
)

data class ListingResponse(
    val status: String,
    val data: Listing
)

data class SearchResponse(
    val status: String,
    val query: String,
    val data: List<Listing>
)

data class HealthResponse(
    val status: String
)

data class Listing(
    val id: Int,
    val title: String,
    val price: Int,
    val category: String
)