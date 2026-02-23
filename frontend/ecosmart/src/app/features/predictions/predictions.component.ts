import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxEchartsDirective, provideEcharts } from 'ngx-echarts';
import { EChartsOption } from 'echarts';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-predictions',
  standalone: true,
  imports: [CommonModule, NgxEchartsDirective, LoadingSpinnerComponent],
  providers: [provideEcharts()],
  template: `
    <div class="page-header">
      <h1>Energy Predictions</h1>
      <p>ML-powered forecasts for your energy consumption</p>
    </div>

    <app-loading-spinner *ngIf="loading"></app-loading-spinner>

    <ng-container *ngIf="!loading">
      <div *ngIf="error" class="error-card">
        <p>{{ error }}</p>
      </div>

      <div class="charts-grid" *ngIf="!error">
        <div class="chart-card">
          <h3>7-Day Forecast</h3>
          <div echarts [options]="forecastChartOptions" class="chart-container"></div>
        </div>
        <div class="chart-card">
          <h3>Monthly Forecast Breakdown</h3>
          <div class="monthly-summary" *ngIf="monthlyPrediction">
            <div class="monthly-value">
              {{ monthlyPrediction.monthly_predicted_kwh | number:'1.0-0' }}
              <small>kWh predicted this month</small>
            </div>
          </div>
        </div>
      </div>

      <div class="chart-card" *ngIf="predictions.length" style="margin-bottom: 28px;">
        <h3>Prediction Details</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Predicted (kWh)</th>
              <th>Lower Bound</th>
              <th>Upper Bound</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let p of predictions">
              <td>{{ p.date }}</td>
              <td><strong>{{ p.predicted_kwh | number:'1.2-2' }}</strong></td>
              <td>{{ p.confidence_lower | number:'1.2-2' }}</td>
              <td>{{ p.confidence_upper | number:'1.2-2' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="chart-card" *ngIf="modelMetrics">
        <h3>Model Performance</h3>
        <div class="metrics-grid">
          <div class="metric" *ngFor="let m of modelMetrics">
            <div class="metric__name">{{ m.name }}</div>
            <div class="metric__values">
              <span>R² = {{ m.r2 | number:'1.4-4' }}</span>
              <span>MAE = {{ m.mae | number:'1.2-2' }} kWh</span>
              <span>RMSE = {{ m.rmse | number:'1.2-2' }} kWh</span>
            </div>
            <div class="metric__bar">
              <div class="metric__fill" [style.width.%]="m.r2 * 100"
                   [class.best]="m.r2 === bestR2"></div>
            </div>
          </div>
        </div>
      </div>
    </ng-container>
  `,
  styles: [`
    .error-card {
      background: #fef2f2;
      border: 1px solid #fecaca;
      color: #dc2626;
      padding: 20px;
      border-radius: 12px;
      margin-bottom: 24px;
    }
    .monthly-summary {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 280px;
    }
    .monthly-value {
      font-size: 56px;
      font-weight: 800;
      color: #3b82f6;
      text-align: center;
      small {
        display: block;
        font-size: 16px;
        color: #94a3b8;
        font-weight: 400;
        margin-top: 8px;
      }
    }
    .metrics-grid {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .metric {
      padding: 16px;
      background: #f8fafc;
      border-radius: 10px;
    }
    .metric__name {
      font-weight: 700;
      font-size: 15px;
      margin-bottom: 8px;
    }
    .metric__values {
      display: flex;
      gap: 24px;
      font-size: 13px;
      color: #64748b;
      margin-bottom: 8px;
    }
    .metric__bar {
      height: 8px;
      background: #e2e8f0;
      border-radius: 4px;
      overflow: hidden;
    }
    .metric__fill {
      height: 100%;
      background: #94a3b8;
      border-radius: 4px;
      transition: width 0.6s ease;
    }
    .metric__fill.best { background: #10b981; }
  `]
})
export class PredictionsComponent implements OnInit {
  loading = true;
  error = '';
  predictions: any[] = [];
  monthlyPrediction: any = null;
  modelMetrics: any[] | null = null;
  bestR2 = 0;
  forecastChartOptions: EChartsOption = {};

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.loading = true;

    this.api.getDailyPredictions(1, 7).subscribe({
      next: (data: any) => {
        if (data.error) {
          this.error = data.error;
          this.loading = false;
          return;
        }
        this.predictions = data;
        this.buildForecastChart(data);
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load predictions. Make sure the ML model is trained.';
        this.loading = false;
      }
    });

    this.api.getMonthlyPrediction(1).subscribe({
      next: (data: any) => {
        if (!data.error) this.monthlyPrediction = data;
      }
    });

    this.api.getModelMetrics().subscribe({
      next: (data: any) => {
        if (!data.error && Array.isArray(data)) {
          this.modelMetrics = data;
          this.bestR2 = Math.max(...data.map((m: any) => m.r2));
        }
      }
    });
  }

  buildForecastChart(data: any[]) {
    this.forecastChartOptions = {
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: data.map(d => d.date),
        axisLabel: { color: '#94a3b8' },
      },
      yAxis: {
        type: 'value',
        name: 'kWh',
        axisLabel: { color: '#94a3b8' },
        splitLine: { lineStyle: { color: '#f1f5f9' } },
      },
      series: [
        {
          name: 'Upper Bound',
          type: 'line',
          data: data.map(d => d.confidence_upper),
          lineStyle: { opacity: 0 },
          areaStyle: { color: 'rgba(59, 130, 246, 0.15)' },
          stack: 'confidence',
          symbol: 'none',
        },
        {
          name: 'Predicted',
          type: 'line',
          data: data.map(d => d.predicted_kwh),
          smooth: true,
          lineStyle: { color: '#3b82f6', width: 3 },
          itemStyle: { color: '#3b82f6' },
          areaStyle: { color: 'rgba(59, 130, 246, 0.05)' },
        },
        {
          name: 'Lower Bound',
          type: 'line',
          data: data.map(d => d.confidence_lower),
          lineStyle: { opacity: 0, type: 'dashed' },
          symbol: 'none',
        },
      ],
      legend: { bottom: 0, textStyle: { color: '#64748b' } },
      grid: { left: 50, right: 20, top: 30, bottom: 50 },
    };
  }
}
