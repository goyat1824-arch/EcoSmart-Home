import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-recommendations',
  standalone: true,
  imports: [CommonModule, LoadingSpinnerComponent],
  template: `
    <div class="page-header">
      <h1>Energy Saving Recommendations</h1>
      <p>Personalized suggestions to reduce your energy consumption and costs</p>
    </div>

    <app-loading-spinner *ngIf="loading"></app-loading-spinner>

    <ng-container *ngIf="!loading">
      <div class="rec-grid">
        <div class="rec-card" *ngFor="let rec of recommendations" [class]="'priority-' + rec.priority">
          <div class="rec-header">
            <span class="rec-category" [class]="'cat-' + rec.category">{{ rec.category }}</span>
            <span class="rec-priority" [class]="'pri-' + rec.priority">{{ rec.priority }}</span>
          </div>
          <h3 class="rec-title">{{ rec.title }}</h3>
          <p class="rec-desc">{{ rec.description }}</p>
          <div class="rec-savings" *ngIf="rec.potential_savings_kwh > 0">
            <div class="saving-item">
              <span class="saving-value">{{ rec.potential_savings_kwh | number:'1.0-0' }}</span>
              <span class="saving-label">kWh/month saved</span>
            </div>
            <div class="saving-item">
              <span class="saving-value saving-cost">€{{ rec.potential_savings_cost | number:'1.2-2' }}</span>
              <span class="saving-label">cost savings</span>
            </div>
          </div>
        </div>
      </div>

      <div class="total-savings" *ngIf="recommendations.length">
        <h3>Total Potential Savings</h3>
        <div class="total-grid">
          <div class="total-item">
            <span class="total-value">{{ totalSavingsKwh | number:'1.0-0' }}</span>
            <span>kWh/month</span>
          </div>
          <div class="total-item">
            <span class="total-value">€{{ totalSavingsCost | number:'1.2-2' }}</span>
            <span>cost/month</span>
          </div>
          <div class="total-item">
            <span class="total-value">{{ totalSavingsKwh * 0.055 | number:'1.1-1' }}</span>
            <span>kg CO2/month</span>
          </div>
        </div>
      </div>
    </ng-container>
  `,
  styles: [`
    .rec-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-bottom: 28px;
    }
    .rec-card {
      background: white;
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      border-left: 4px solid #e2e8f0;
      transition: transform 0.2s;
    }
    .rec-card:hover { transform: translateY(-2px); }
    .rec-card.priority-high { border-left-color: #ef4444; }
    .rec-card.priority-medium { border-left-color: #f59e0b; }
    .rec-card.priority-low { border-left-color: #10b981; }

    .rec-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .rec-category {
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .cat-efficiency { background: #dbeafe; color: #1e40af; }
    .cat-behavior { background: #fef3c7; color: #92400e; }
    .cat-upgrade { background: #f3e8ff; color: #6b21a8; }
    .cat-scheduling { background: #d1fae5; color: #065f46; }

    .rec-priority {
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
    }
    .pri-high { background: #fee2e2; color: #dc2626; }
    .pri-medium { background: #fef3c7; color: #d97706; }
    .pri-low { background: #d1fae5; color: #059669; }

    .rec-title {
      font-size: 17px;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 8px;
    }
    .rec-desc {
      font-size: 14px;
      color: #64748b;
      line-height: 1.5;
      margin-bottom: 16px;
    }
    .rec-savings {
      display: flex;
      gap: 24px;
      padding-top: 16px;
      border-top: 1px solid #f1f5f9;
    }
    .saving-item {
      display: flex;
      flex-direction: column;
    }
    .saving-value {
      font-size: 20px;
      font-weight: 700;
      color: #10b981;
    }
    .saving-cost { color: #f59e0b; }
    .saving-label {
      font-size: 12px;
      color: #94a3b8;
    }

    .total-savings {
      background: white;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      text-align: center;
    }
    .total-savings h3 {
      font-size: 18px;
      color: #334155;
      margin-bottom: 20px;
    }
    .total-grid {
      display: flex;
      justify-content: center;
      gap: 48px;
    }
    .total-item {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .total-value {
      font-size: 32px;
      font-weight: 800;
      color: #10b981;
    }
    .total-item span:last-child {
      font-size: 13px;
      color: #94a3b8;
      margin-top: 4px;
    }
  `]
})
export class RecommendationsComponent implements OnInit {
  loading = true;
  recommendations: any[] = [];
  totalSavingsKwh = 0;
  totalSavingsCost = 0;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.loading = true;
    this.api.getRecommendations(1).subscribe({
      next: (data) => {
        this.recommendations = data;
        this.totalSavingsKwh = data.reduce((sum: number, r: any) => sum + (r.potential_savings_kwh || 0), 0);
        this.totalSavingsCost = data.reduce((sum: number, r: any) => sum + (r.potential_savings_cost || 0), 0);
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }
}
