import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxEchartsDirective, provideEcharts } from 'ngx-echarts';
import { EChartsOption } from 'echarts';
import { StatCardComponent } from '../../shared/components/stat-card/stat-card.component';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule, NgxEchartsDirective, StatCardComponent, LoadingSpinnerComponent],
  providers: [provideEcharts()],
  template: `
    <div class="page-header">
      <h1>Analytics</h1>
      <p>CO2 emissions, cost analysis, and sustainability insights</p>
    </div>

    <app-loading-spinner *ngIf="loading"></app-loading-spinner>

    <ng-container *ngIf="!loading">
      <!-- Sustainability Score -->
      <div class="score-section" *ngIf="sustainability">
        <div class="score-card">
          <div class="score-circle" [class]="'grade-' + sustainability.grade?.charAt(0)?.toLowerCase()">
            <span class="score-value">{{ sustainability.score }}</span>
            <span class="score-grade">{{ sustainability.grade }}</span>
          </div>
          <div class="score-details">
            <h3>Sustainability Score</h3>
            <p>Average daily: <strong>{{ sustainability.avg_daily_kwh }} kWh</strong></p>
            <p>Baseline: <strong>{{ sustainability.baseline_daily_kwh }} kWh</strong></p>
            <p>Trend: <strong class="trend" [class]="sustainability.trend">{{ sustainability.trend }}</strong></p>
            <p *ngIf="sustainability.co2_saved_kg > 0">CO2 Saved: <strong class="co2-saved">{{ sustainability.co2_saved_kg }} kg</strong></p>
          </div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card">
          <h3>CO2 Emissions Over Time</h3>
          <div echarts [options]="co2ChartOptions" class="chart-container"></div>
        </div>
        <div class="chart-card">
          <h3>Monthly Cost Analysis</h3>
          <div echarts [options]="costChartOptions" class="chart-container"></div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card" style="grid-column: 1 / -1;">
          <h3>Energy vs Cost vs CO2 - Monthly Comparison</h3>
          <div echarts [options]="comparisonChartOptions" class="chart-container" style="height: 400px;"></div>
        </div>
      </div>
    </ng-container>
  `,
  styles: [`
    .score-section {
      margin-bottom: 28px;
    }
    .score-card {
      background: white;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      display: flex;
      align-items: center;
      gap: 32px;
    }
    .score-circle {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: #f0fdf4;
      border: 4px solid #10b981;
    }
    .score-circle.grade-a { border-color: #10b981; background: #f0fdf4; }
    .score-circle.grade-b { border-color: #3b82f6; background: #eff6ff; }
    .score-circle.grade-c { border-color: #f59e0b; background: #fffbeb; }
    .score-circle.grade-d { border-color: #ef4444; background: #fef2f2; }
    .score-circle.grade-f { border-color: #dc2626; background: #fef2f2; }
    .score-value {
      font-size: 36px;
      font-weight: 800;
      color: #0f172a;
    }
    .score-grade {
      font-size: 18px;
      font-weight: 700;
      color: #64748b;
    }
    .score-details h3 {
      font-size: 20px;
      margin-bottom: 12px;
    }
    .score-details p {
      color: #64748b;
      margin-bottom: 6px;
      font-size: 14px;
    }
    .trend.improving { color: #10b981; }
    .trend.declining { color: #ef4444; }
    .trend.stable { color: #f59e0b; }
    .co2-saved { color: #10b981; }
  `]
})
export class AnalyticsComponent implements OnInit {
  loading = true;
  sustainability: any = null;
  co2ChartOptions: EChartsOption = {};
  costChartOptions: EChartsOption = {};
  comparisonChartOptions: EChartsOption = {};

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.loading = true;

    this.api.getSustainabilityScore(1).subscribe({
      next: (data) => {
        this.sustainability = data;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });

    this.api.getCO2Data(1).subscribe({
      next: (data) => {
        const monthly = this.aggregateMonthly(data, 'co2_kg');
        this.co2ChartOptions = {
          tooltip: { trigger: 'axis' },
          xAxis: {
            type: 'category',
            data: monthly.map(d => d.month),
            axisLabel: { color: '#94a3b8', rotate: 45 },
          },
          yAxis: {
            type: 'value',
            name: 'kg CO2',
            axisLabel: { color: '#94a3b8' },
            splitLine: { lineStyle: { color: '#f1f5f9' } },
          },
          series: [{
            data: monthly.map(d => d.value),
            type: 'bar',
            itemStyle: {
              color: '#10b981',
              borderRadius: [6, 6, 0, 0],
            },
          }],
          grid: { left: 60, right: 20, top: 30, bottom: 60 },
        };
      }
    });

    this.api.getCostData(1).subscribe({
      next: (data) => {
        const monthly = this.aggregateMonthly(data, 'cost');
        this.costChartOptions = {
          tooltip: { trigger: 'axis' },
          xAxis: {
            type: 'category',
            data: monthly.map(d => d.month),
            axisLabel: { color: '#94a3b8', rotate: 45 },
          },
          yAxis: {
            type: 'value',
            name: 'Cost (EUR)',
            axisLabel: { color: '#94a3b8' },
            splitLine: { lineStyle: { color: '#f1f5f9' } },
          },
          series: [{
            data: monthly.map(d => d.value),
            type: 'line',
            smooth: true,
            areaStyle: { color: 'rgba(245, 158, 11, 0.1)' },
            lineStyle: { color: '#f59e0b', width: 3 },
            itemStyle: { color: '#f59e0b' },
          }],
          grid: { left: 60, right: 20, top: 30, bottom: 60 },
        };
      }
    });

    this.api.getMonthlyTrend(1, 24).subscribe({
      next: (data) => {
        this.comparisonChartOptions = {
          tooltip: { trigger: 'axis' },
          legend: { bottom: 0, textStyle: { color: '#64748b' } },
          xAxis: {
            type: 'category',
            data: data.map((d: any) => d.month),
            axisLabel: { color: '#94a3b8', rotate: 45 },
          },
          yAxis: [
            { type: 'value', name: 'kWh', axisLabel: { color: '#94a3b8' }, splitLine: { lineStyle: { color: '#f1f5f9' } } },
            { type: 'value', name: 'EUR / kg', axisLabel: { color: '#94a3b8' }, splitLine: { show: false } },
          ],
          series: [
            {
              name: 'Energy (kWh)',
              type: 'bar',
              data: data.map((d: any) => d.total_kwh),
              itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] },
            },
            {
              name: 'Cost (EUR)',
              type: 'line',
              yAxisIndex: 1,
              data: data.map((d: any) => d.cost),
              smooth: true,
              lineStyle: { color: '#f59e0b', width: 2 },
              itemStyle: { color: '#f59e0b' },
            },
            {
              name: 'CO2 (kg)',
              type: 'line',
              yAxisIndex: 1,
              data: data.map((d: any) => d.co2_kg),
              smooth: true,
              lineStyle: { color: '#10b981', width: 2 },
              itemStyle: { color: '#10b981' },
            },
          ],
          grid: { left: 60, right: 60, top: 30, bottom: 60 },
        };
      }
    });
  }

  private aggregateMonthly(data: any[], valueKey: string): { month: string; value: number }[] {
    const grouped: Record<string, number> = {};
    for (const d of data) {
      const month = d.date.substring(0, 7);
      grouped[month] = (grouped[month] || 0) + d[valueKey];
    }
    return Object.entries(grouped)
      .map(([month, value]) => ({ month, value: Math.round(value * 100) / 100 }))
      .sort((a, b) => a.month.localeCompare(b.month));
  }
}
