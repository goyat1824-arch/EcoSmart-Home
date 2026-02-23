import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxEchartsDirective, provideEcharts } from 'ngx-echarts';
import { EChartsOption } from 'echarts';
import { StatCardComponent } from '../../shared/components/stat-card/stat-card.component';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, NgxEchartsDirective, StatCardComponent, LoadingSpinnerComponent],
  providers: [provideEcharts()],
  template: `
    <div class="page-header">
      <h1>Dashboard</h1>
      <p>Real-time overview of your household energy intelligence</p>
    </div>

    <app-loading-spinner *ngIf="loading"></app-loading-spinner>

    <ng-container *ngIf="!loading">
      <div class="stats-grid">
        <app-stat-card
          icon="&#9889;" label="Today's Usage" [value]="summary.today_kwh" unit="kWh"
          [change]="summary.daily_change_pct" color="blue">
        </app-stat-card>
        <app-stat-card
          icon="&#127793;" label="CO2 This Month" [value]="summary.monthly_co2_kg" unit="kg"
          color="green">
        </app-stat-card>
        <app-stat-card
          icon="&#128176;" label="Monthly Cost" [value]="'€' + summary.monthly_cost"
          color="orange">
        </app-stat-card>
        <app-stat-card
          icon="&#11088;" label="Sustainability" [value]="summary.sustainability_score + ' (' + summary.sustainability_grade + ')'"
          color="purple">
        </app-stat-card>
      </div>

      <div class="charts-grid">
        <div class="chart-card">
          <h3>7-Day Consumption Trend</h3>
          <div echarts [options]="trendChartOptions" class="chart-container"></div>
        </div>
        <div class="chart-card">
          <h3>Appliance Breakdown</h3>
          <div echarts [options]="pieChartOptions" class="chart-container"></div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card">
          <h3>Monthly Energy Trend</h3>
          <div echarts [options]="monthlyChartOptions" class="chart-container"></div>
        </div>
        <div class="chart-card">
          <h3>Tomorrow's Prediction</h3>
          <div class="prediction-card">
            <div class="prediction-value">{{ summary.predicted_tomorrow_kwh }} <small>kWh</small></div>
            <p class="prediction-label">Predicted consumption for tomorrow</p>
            <div class="prediction-avg">7-day average: {{ summary.avg_daily_kwh_7d }} kWh</div>
          </div>
        </div>
      </div>
    </ng-container>
  `,
  styles: [`
    .prediction-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 280px;
    }
    .prediction-value {
      font-size: 64px;
      font-weight: 800;
      color: #10b981;
      small { font-size: 24px; color: #94a3b8; font-weight: 400; }
    }
    .prediction-label {
      font-size: 15px;
      color: #64748b;
      margin-top: 8px;
    }
    .prediction-avg {
      margin-top: 16px;
      padding: 8px 20px;
      background: #f0fdf4;
      border-radius: 20px;
      color: #065f46;
      font-weight: 600;
      font-size: 14px;
    }
  `]
})
export class DashboardComponent implements OnInit {
  loading = true;
  summary: any = {};
  trendChartOptions: EChartsOption = {};
  pieChartOptions: EChartsOption = {};
  monthlyChartOptions: EChartsOption = {};

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.loading = true;

    // Load dashboard summary
    this.api.getDashboardSummary(1).subscribe({
      next: (data) => {
        this.summary = data;
        this.loading = false;
      },
      error: () => {
        this.summary = {
          today_kwh: 0, yesterday_kwh: 0, daily_change_pct: 0,
          monthly_kwh: 0, monthly_cost: 0, monthly_co2_kg: 0,
          sustainability_score: 50, sustainability_grade: 'C',
          predicted_tomorrow_kwh: 0, avg_daily_kwh_7d: 0,
        };
        this.loading = false;
      }
    });

    // Load 7-day trend
    this.api.getDailySummary(1).subscribe({
      next: (data) => {
        const recent = data.slice(-7);
        this.trendChartOptions = {
          tooltip: { trigger: 'axis' },
          xAxis: {
            type: 'category',
            data: recent.map((d: any) => d.date.slice(5)),
            axisLabel: { color: '#94a3b8' },
          },
          yAxis: {
            type: 'value',
            name: 'kWh',
            axisLabel: { color: '#94a3b8' },
            splitLine: { lineStyle: { color: '#f1f5f9' } },
          },
          series: [{
            data: recent.map((d: any) => d.total_kwh),
            type: 'line',
            smooth: true,
            areaStyle: { color: 'rgba(16, 185, 129, 0.1)' },
            lineStyle: { color: '#10b981', width: 3 },
            itemStyle: { color: '#10b981' },
          }],
          grid: { left: 50, right: 20, top: 30, bottom: 30 },
        };
      }
    });

    // Load appliance breakdown
    this.api.getApplianceBreakdown(1).subscribe({
      next: (data) => {
        this.pieChartOptions = {
          tooltip: { trigger: 'item', formatter: '{b}: {c} kWh ({d}%)' },
          series: [{
            type: 'pie',
            radius: ['45%', '75%'],
            avoidLabelOverlap: true,
            itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
            label: { show: true, formatter: '{b}\n{d}%' },
            data: data.map((d: any) => ({
              name: d.category,
              value: d.kwh,
            })),
          }],
          color: ['#f59e0b', '#3b82f6', '#ef4444', '#8b5cf6'],
        };
      }
    });

    // Load monthly trend
    this.api.getMonthlyTrend(1, 12).subscribe({
      next: (data) => {
        this.monthlyChartOptions = {
          tooltip: { trigger: 'axis' },
          xAxis: {
            type: 'category',
            data: data.map((d: any) => d.month),
            axisLabel: { color: '#94a3b8', rotate: 45 },
          },
          yAxis: [
            {
              type: 'value',
              name: 'kWh',
              axisLabel: { color: '#94a3b8' },
              splitLine: { lineStyle: { color: '#f1f5f9' } },
            },
            {
              type: 'value',
              name: 'Cost (€)',
              axisLabel: { color: '#94a3b8' },
              splitLine: { show: false },
            },
          ],
          series: [
            {
              name: 'Energy (kWh)',
              data: data.map((d: any) => d.total_kwh),
              type: 'bar',
              itemStyle: { color: '#3b82f6', borderRadius: [6, 6, 0, 0] },
            },
            {
              name: 'Cost (€)',
              data: data.map((d: any) => d.cost),
              type: 'line',
              yAxisIndex: 1,
              smooth: true,
              lineStyle: { color: '#f59e0b', width: 2 },
              itemStyle: { color: '#f59e0b' },
            },
          ],
          legend: { bottom: 0, textStyle: { color: '#64748b' } },
          grid: { left: 60, right: 60, top: 30, bottom: 50 },
        };
      }
    });
  }
}
