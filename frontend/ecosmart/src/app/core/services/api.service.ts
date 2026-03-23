import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

const API_BASE = environment.apiBase;

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  // --- Users ---
  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${API_BASE}/users/`);
  }

  // --- Households ---
  getHouseholds(userId?: number): Observable<any[]> {
    let params = new HttpParams();
    if (userId) params = params.set('user_id', userId);
    return this.http.get<any[]>(`${API_BASE}/households/`, { params });
  }

  getHousehold(id: number): Observable<any> {
    return this.http.get<any>(`${API_BASE}/households/${id}`);
  }

  updateHousehold(id: number, data: any): Observable<any> {
    return this.http.put<any>(`${API_BASE}/households/${id}`, data);
  }

  // --- Appliances ---
  getAppliances(householdId?: number): Observable<any[]> {
    let params = new HttpParams();
    if (householdId) params = params.set('household_id', householdId);
    return this.http.get<any[]>(`${API_BASE}/appliances/`, { params });
  }

  createAppliance(data: any): Observable<any> {
    return this.http.post<any>(`${API_BASE}/appliances/`, data);
  }

  updateAppliance(id: number, data: any): Observable<any> {
    return this.http.put<any>(`${API_BASE}/appliances/${id}`, data);
  }

  deleteAppliance(id: number): Observable<void> {
    return this.http.delete<void>(`${API_BASE}/appliances/${id}`);
  }

  // --- Energy Readings ---
  getEnergyReadings(householdId: number, startDate?: string, endDate?: string, limit = 365): Observable<any[]> {
    let params = new HttpParams().set('household_id', householdId).set('limit', limit);
    if (startDate) params = params.set('start_date', startDate);
    if (endDate) params = params.set('end_date', endDate);
    return this.http.get<any[]>(`${API_BASE}/energy/`, { params });
  }

  getDailySummary(householdId: number, startDate?: string, endDate?: string): Observable<any[]> {
    let params = new HttpParams().set('household_id', householdId);
    if (startDate) params = params.set('start_date', startDate);
    if (endDate) params = params.set('end_date', endDate);
    return this.http.get<any[]>(`${API_BASE}/energy/daily-summary`, { params });
  }

  // --- Analytics ---
  getDashboardSummary(householdId: number): Observable<any> {
    return this.http.get<any>(`${API_BASE}/analytics/summary`, {
      params: new HttpParams().set('household_id', householdId)
    });
  }

  getCO2Data(householdId: number, startDate?: string, endDate?: string): Observable<any[]> {
    let params = new HttpParams().set('household_id', householdId);
    if (startDate) params = params.set('start_date', startDate);
    if (endDate) params = params.set('end_date', endDate);
    return this.http.get<any[]>(`${API_BASE}/analytics/co2`, { params });
  }

  getCostData(householdId: number, startDate?: string, endDate?: string): Observable<any[]> {
    let params = new HttpParams().set('household_id', householdId);
    if (startDate) params = params.set('start_date', startDate);
    if (endDate) params = params.set('end_date', endDate);
    return this.http.get<any[]>(`${API_BASE}/analytics/cost`, { params });
  }

  getSustainabilityScore(householdId: number): Observable<any> {
    return this.http.get<any>(`${API_BASE}/analytics/sustainability-score`, {
      params: new HttpParams().set('household_id', householdId)
    });
  }

  getMonthlyTrend(householdId: number, months = 12): Observable<any[]> {
    return this.http.get<any[]>(`${API_BASE}/analytics/monthly-trend`, {
      params: new HttpParams().set('household_id', householdId).set('months', months)
    });
  }

  getApplianceBreakdown(householdId: number, startDate?: string, endDate?: string): Observable<any[]> {
    let params = new HttpParams().set('household_id', householdId);
    if (startDate) params = params.set('start_date', startDate);
    if (endDate) params = params.set('end_date', endDate);
    return this.http.get<any[]>(`${API_BASE}/analytics/appliance-breakdown`, { params });
  }

  // --- Predictions ---
  getDailyPredictions(householdId: number, days = 7): Observable<any[]> {
    return this.http.get<any[]>(`${API_BASE}/predictions/daily`, {
      params: new HttpParams().set('household_id', householdId).set('days', days)
    });
  }

  getMonthlyPrediction(householdId: number): Observable<any> {
    return this.http.get<any>(`${API_BASE}/predictions/monthly`, {
      params: new HttpParams().set('household_id', householdId)
    });
  }

  getModelMetrics(): Observable<any> {
    return this.http.get<any>(`${API_BASE}/predictions/model-metrics`);
  }

  // --- Recommendations ---
  getRecommendations(householdId: number): Observable<any[]> {
    return this.http.get<any[]>(`${API_BASE}/recommendations/`, {
      params: new HttpParams().set('household_id', householdId)
    });
  }
}
