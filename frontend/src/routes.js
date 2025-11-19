import { Children, Component } from "react";
import MainLayout from "./pages/MainLayout";
import HomePage from "./pages/HomePage";
import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
    {
        Component:MainLayout,
        children:[
            {
                index:true,
                Component:HomePage
            }
        ]

    }
    
]
    
)