package com.olx.scraper

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Category
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Settings
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.olx.scraper.ui.screens.HomeScreen
import com.olx.scraper.ui.screens.CategoriesScreen
import com.olx.scraper.ui.screens.FavoritesScreen
import com.olx.scraper.ui.screens.SettingsScreen

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Surface(color = MaterialTheme.colorScheme.background) {
                val navController = rememberNavController()

                Scaffold(
                    bottomBar = {
                        NavigationBar {
                            NavigationBarItem(
                                icon = { Icon(Icons.Default.Home, "Home") },
                                label = { Text("Home") },
                                selected = false,
                                onClick = { navController.navigate("home") }
                            )
                            NavigationBarItem(
                                icon = { Icon(Icons.Default.Category, "Categories") },
                                label = { Text("Categories") },
                                selected = false,
                                onClick = { navController.navigate("categories") }
                            )
                            NavigationBarItem(
                                icon = { Icon(Icons.Default.Favorite, "Favorites") },
                                label = { Text("Favorites") },
                                selected = false,
                                onClick = { navController.navigate("favorites") }
                            )
                            NavigationBarItem(
                                icon = { Icon(Icons.Default.Settings, "Settings") },
                                label = { Text("Settings") },
                                selected = false,
                                onClick = { navController.navigate("settings") }
                            )
                        }
                    }
                ) { innerPadding ->
                    Box(modifier = Modifier.padding(innerPadding)) {
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
                }
            }
        }
    }
}