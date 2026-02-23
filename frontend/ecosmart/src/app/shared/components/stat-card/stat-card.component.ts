import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="stat-card" [class]="'stat-card--' + color">
      <div class="stat-card__icon">{{ icon }}</div>
      <div class="stat-card__content">
        <span class="stat-card__label">{{ label }}</span>
        <span class="stat-card__value">{{ value }}<small *ngIf="unit"> {{ unit }}</small></span>
        <span class="stat-card__change" *ngIf="change !== undefined"
              [class.positive]="change <= 0"
              [class.negative]="change > 0">
          {{ change > 0 ? '+' : '' }}{{ change | number:'1.1-1' }}%
        </span>
      </div>
    </div>
  `,
  styles: [`
    .stat-card {
      background: white;
      border-radius: 16px;
      padding: 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      transition: transform 0.2s, box-shadow 0.2s;
      border-left: 4px solid #e0e0e0;
    }
    .stat-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .stat-card--green { border-left-color: #10b981; }
    .stat-card--blue { border-left-color: #3b82f6; }
    .stat-card--orange { border-left-color: #f59e0b; }
    .stat-card--red { border-left-color: #ef4444; }
    .stat-card--purple { border-left-color: #8b5cf6; }

    .stat-card__icon {
      font-size: 32px;
      width: 56px;
      height: 56px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 12px;
      background: #f8fafc;
    }
    .stat-card__content {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .stat-card__label {
      font-size: 13px;
      color: #64748b;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .stat-card__value {
      font-size: 28px;
      font-weight: 700;
      color: #1e293b;
    }
    .stat-card__value small {
      font-size: 14px;
      font-weight: 400;
      color: #94a3b8;
    }
    .stat-card__change {
      font-size: 13px;
      font-weight: 600;
    }
    .stat-card__change.positive { color: #10b981; }
    .stat-card__change.negative { color: #ef4444; }
  `]
})
export class StatCardComponent {
  @Input() icon = '';
  @Input() label = '';
  @Input() value: string | number = '';
  @Input() unit = '';
  @Input() change?: number;
  @Input() color: 'green' | 'blue' | 'orange' | 'red' | 'purple' = 'green';
}
