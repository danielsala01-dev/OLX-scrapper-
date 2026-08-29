package com.olx.scraper.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.olx.scraper.ui.screens.HomeScreen
import com.olx.scraper.ui.screens.CategoriesScreen
import com.olx.scraper.ui.screens.FavoritesScreen
import com.olx.scraper.ui.screens.SettingsScreen

@Composable
fun OLXNavGraph() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = "home"
    ) {
        composable("home") {
            HomeScreen(navController)
        }
        composable("categories") {
            CategoriesScreen(navController)
        }
        composable("favorites") {
            FavoritesScreen(navController)
        }
        composable("settings") {
            SettingsScreen(navController)
        }
    }
}