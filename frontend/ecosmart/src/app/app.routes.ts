import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
  },
  {
    path: 'energy',
    loadComponent: () => import('./features/energy/energy.component').then(m => m.EnergyComponent),
  },
  {
    path: 'predictions',
    loadComponent: () => import('./features/predictions/predictions.component').then(m => m.PredictionsComponent),
  },
  {
    path: 'analytics',
    loadComponent: () => import('./features/analytics/analytics.component').then(m => m.AnalyticsComponent),
  },
  {
    path: 'households',
    loadComponent: () => import('./features/households/households.component').then(m => m.HouseholdsComponent),
  },
  {
    path: 'recommendations',
    loadComponent: () => import('./features/recommendations/recommendations.component').then(m => m.RecommendationsComponent),
  },
];
