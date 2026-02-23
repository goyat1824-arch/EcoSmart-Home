import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgxEchartsDirective, provideEcharts } from 'ngx-echarts';
import { EChartsOption } from 'echarts';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-energy',
  standalone: true,
  imports: [CommonModule, FormsModule, NgxEchartsDirective, LoadingSpinnerComponent],
  providers: [provideEcharts()],
  template: `
    <div class="page-header">
      <h1>Energy History</h1>
      <p>Track and analyze your household energy consumption over time</p>
    </div>

    <div class="filters">
      <div class="form-group">
        <label>Start Date</label>
        <input type="date" [(ngModel)]="startDate" (change)="loadData()">
      </div>
      <div class="form-group">
        <label>End Date</label>
        <input type="date" [(ngModel)]="endDate" (change)="loadData()">
      </div>
    </div>

    <app-loading-spinner *ngIf="loading"></app-loading-spinner>

    <ng-container *ngIf="!loading">
      <div class="charts-grid">
        <div class="chart-card">
          <h3>Daily Energy Consumption</h3>
          <div echarts [options]="dailyChartOptions" class="chart-container"></div>
        </div>
        <div class="chart-card">
          <h3>Appliance Category Breakdown</h3>
          <div echarts [options]="stackedChartOptions" class="chart-container"></div>
        </div>
      </div>

      <div class="chart-card" style="margin-bottom: 28px;">
        <h3>Energy Consumption Data</h3>
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Total (kWh)</th>
                <th>Kitchen</th>
                <th>Laundry</th>
                <th>HVAC</th>
                <th>Peak Hour</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let reading of readings.slice(0, 50)">
                <td>{{ reading.date }}</td>
                <td><strong>{{ reading.total_kwh | number:'1.2-2' }}</strong></td>
                <td>{{ reading.kitchen_kwh | number:'1.2-2' }}</td>
                <td>{{ reading.laundry_kwh | number:'1.2-2' }}</td>
                <td>{{ reading.hvac_kwh | number:'1.2-2' }}</td>
                <td>{{ reading.peak_hour }}:00</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </ng-container>
  `,
  styles: [`
    .filters {
      display: flex;
      gap: 16px;
      margin-bottom: 24px;
    }
    .filters .form-group {
      min-width: 180px;
    }
    .table-wrapper {
      max-height: 400px;
      overflow-y: auto;
    }
  `]
})
export class EnergyComponent implements OnInit {
  loading = true;
  startDate = '';
  endDate = '';
  readings: any[] = [];
  dailyChartOptions: EChartsOption = {};
  stackedChartOptions: EChartsOption = {};

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.loading = true;
    this.api.getDailySummary(1, this.startDate || undefined, this.endDate || undefined).subscribe({
      next: (data) => {
        this.readings = data;
        this.buildCharts(data);
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  buildCharts(data: any[]) {
    const recent = data.slice(-90);
    const dates = recent.map(d => d.date);

    this.dailyChartOptions = {
      tooltip: { trigger: 'axis' },
      dataZoom: [{ type: 'slider', start: 70, end: 100 }],
      xAxis: {
        type: 'category',
        data: dates,
        axisLabel: { color: '#94a3b8' },
      },
      yAxis: {
        type: 'value',
        name: 'kWh',
        axisLabel: { color: '#94a3b8' },
        splitLine: { lineStyle: { color: '#f1f5f9' } },
      },
      series: [{
        data: recent.map(d => d.total_kwh),
        type: 'line',
        smooth: true,
        areaStyle: { color: 'rgba(59, 130, 246, 0.08)' },
        lineStyle: { color: '#3b82f6', width: 2 },
        itemStyle: { color: '#3b82f6' },
      }],
      grid: { left: 50, right: 20, top: 30, bottom: 70 },
    };

    this.stackedChartOptions = {
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: { bottom: 0, textStyle: { color: '#64748b' } },
      dataZoom: [{ type: 'slider', start: 70, end: 100 }],
      xAxis: {
        type: 'category',
        data: dates,
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
          name: 'Kitchen',
          type: 'bar',
          stack: 'total',
          data: recent.map(d => d.kitchen_kwh),
          itemStyle: { color: '#f59e0b' },
        },
        {
          name: 'Laundry',
          type: 'bar',
          stack: 'total',
          data: recent.map(d => d.laundry_kwh),
          itemStyle: { color: '#3b82f6' },
        },
        {
          name: 'HVAC',
          type: 'bar',
          stack: 'total',
          data: recent.map(d => d.hvac_kwh),
          itemStyle: { color: '#ef4444' },
        },
      ],
      grid: { left: 50, right: 20, top: 30, bottom: 70 },
    };
  }
}
