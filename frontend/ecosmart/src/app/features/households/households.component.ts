import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-households',
  standalone: true,
  imports: [CommonModule, FormsModule, LoadingSpinnerComponent],
  template: `
    <div class="page-header">
      <h1>Household & Appliance Management</h1>
      <p>Manage your households and connected appliances</p>
    </div>

    <app-loading-spinner *ngIf="loading"></app-loading-spinner>

    <ng-container *ngIf="!loading">
      <!-- Household Info -->
      <div class="chart-card" *ngIf="household" style="margin-bottom: 28px;">
        <h3>Household Details</h3>
        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-label">Name</span>
            <span class="detail-value">{{ household.name }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Address</span>
            <span class="detail-value">{{ household.address }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">City</span>
            <span class="detail-value">{{ household.city }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Location</span>
            <span class="detail-value">{{ household.latitude }}°N, {{ household.longitude }}°E</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Tariff</span>
            <span class="detail-value">€{{ household.tariff_per_kwh }}/kWh</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Emission Factor</span>
            <span class="detail-value">{{ household.emission_factor }} kg CO2/kWh</span>
          </div>
        </div>
      </div>

      <!-- Appliances -->
      <div class="chart-card" style="margin-bottom: 28px;">
        <div class="section-header">
          <h3>Appliances</h3>
          <button class="btn btn--primary" (click)="showForm = !showForm">
            {{ showForm ? 'Cancel' : '+ Add Appliance' }}
          </button>
        </div>

        <!-- Add Form -->
        <div class="add-form" *ngIf="showForm">
          <div class="form-row">
            <div class="form-group">
              <label>Name</label>
              <input type="text" [(ngModel)]="newAppliance.name" placeholder="e.g., Air Conditioner">
            </div>
            <div class="form-group">
              <label>Category</label>
              <select [(ngModel)]="newAppliance.category">
                <option value="Kitchen">Kitchen</option>
                <option value="Laundry">Laundry</option>
                <option value="HVAC">HVAC</option>
                <option value="Lighting">Lighting</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="form-group">
              <label>Watt Rating</label>
              <input type="number" [(ngModel)]="newAppliance.watt_rating" placeholder="e.g., 1500">
            </div>
            <div class="form-group">
              <label>Avg Hours/Day</label>
              <input type="number" [(ngModel)]="newAppliance.avg_usage_hours" placeholder="e.g., 4">
            </div>
            <div class="form-group">
              <label>Efficiency (1-5)</label>
              <select [(ngModel)]="newAppliance.efficiency_rating">
                <option [value]="1">1 Star</option>
                <option [value]="2">2 Stars</option>
                <option [value]="3">3 Stars</option>
                <option [value]="4">4 Stars</option>
                <option [value]="5">5 Stars</option>
              </select>
            </div>
          </div>
          <button class="btn btn--primary" (click)="addAppliance()">Add Appliance</button>
        </div>

        <!-- Appliance List -->
        <table class="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Watts</th>
              <th>Hours/Day</th>
              <th>Daily kWh</th>
              <th>Efficiency</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let a of appliances">
              <td><strong>{{ a.name }}</strong></td>
              <td><span class="category-badge" [class]="'cat-' + a.category.toLowerCase()">{{ a.category }}</span></td>
              <td>{{ a.watt_rating }}W</td>
              <td>{{ a.avg_usage_hours }}h</td>
              <td>{{ (a.watt_rating * a.avg_usage_hours / 1000) | number:'1.2-2' }}</td>
              <td>
                <span class="stars">{{ getStars(a.efficiency_rating) }}</span>
              </td>
              <td>
                <button class="btn btn--danger btn--sm" (click)="deleteAppliance(a.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </ng-container>
  `,
  styles: [`
    .detail-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }
    .detail-item {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .detail-label {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #94a3b8;
      font-weight: 600;
    }
    .detail-value {
      font-size: 16px;
      font-weight: 600;
      color: #1e293b;
    }
    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }
    .add-form {
      background: #f8fafc;
      padding: 20px;
      border-radius: 12px;
      margin-bottom: 20px;
    }
    .form-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }
    .category-badge {
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
    }
    .cat-kitchen { background: #fef3c7; color: #92400e; }
    .cat-laundry { background: #dbeafe; color: #1e40af; }
    .cat-hvac { background: #fee2e2; color: #991b1b; }
    .cat-lighting { background: #fef9c3; color: #854d0e; }
    .cat-other { background: #f1f5f9; color: #475569; }
    .stars { color: #f59e0b; font-size: 16px; }
    .btn--sm { padding: 6px 12px; font-size: 12px; }
  `]
})
export class HouseholdsComponent implements OnInit {
  loading = true;
  household: any = null;
  appliances: any[] = [];
  showForm = false;
  newAppliance = {
    household_id: 1,
    name: '',
    category: 'Kitchen',
    watt_rating: 0,
    avg_usage_hours: 0,
    efficiency_rating: 3,
  };

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.loading = true;
    this.api.getHousehold(1).subscribe({
      next: (data) => {
        this.household = data;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
    this.api.getAppliances(1).subscribe({
      next: (data) => { this.appliances = data; },
    });
  }

  addAppliance() {
    if (!this.newAppliance.name || !this.newAppliance.watt_rating) return;
    this.api.createAppliance(this.newAppliance).subscribe({
      next: () => {
        this.showForm = false;
        this.newAppliance = { household_id: 1, name: '', category: 'Kitchen', watt_rating: 0, avg_usage_hours: 0, efficiency_rating: 3 };
        this.api.getAppliances(1).subscribe(data => this.appliances = data);
      }
    });
  }

  deleteAppliance(id: number) {
    this.api.deleteAppliance(id).subscribe({
      next: () => {
        this.appliances = this.appliances.filter(a => a.id !== id);
      }
    });
  }

  getStars(rating: number): string {
    return '\u2605'.repeat(rating) + '\u2606'.repeat(5 - rating);
  }
}
