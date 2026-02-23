import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  template: `
    <nav class="sidebar">
      <div class="sidebar__brand">
        <span class="sidebar__logo">&#9889;</span>
        <span class="sidebar__title">EcoSmart</span>
      </div>
      <ul class="sidebar__nav">
        <li>
          <a routerLink="/dashboard" routerLinkActive="active">
            <span class="nav-icon">&#9632;</span> Dashboard
          </a>
        </li>
        <li>
          <a routerLink="/energy" routerLinkActive="active">
            <span class="nav-icon">&#9889;</span> Energy History
          </a>
        </li>
        <li>
          <a routerLink="/predictions" routerLinkActive="active">
            <span class="nav-icon">&#9734;</span> Predictions
          </a>
        </li>
        <li>
          <a routerLink="/analytics" routerLinkActive="active">
            <span class="nav-icon">&#9673;</span> Analytics
          </a>
        </li>
        <li>
          <a routerLink="/households" routerLinkActive="active">
            <span class="nav-icon">&#9750;</span> Households
          </a>
        </li>
        <li>
          <a routerLink="/recommendations" routerLinkActive="active">
            <span class="nav-icon">&#10003;</span> Recommendations
          </a>
        </li>
      </ul>
      <div class="sidebar__footer">
        <small>EcoSmart Home v1.0</small>
      </div>
    </nav>
  `,
  styles: [`
    .sidebar {
      width: 240px;
      min-height: 100vh;
      background: linear-gradient(180deg, #064e3b 0%, #065f46 100%);
      color: white;
      display: flex;
      flex-direction: column;
      position: fixed;
      left: 0;
      top: 0;
      z-index: 100;
    }
    .sidebar__brand {
      padding: 24px 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .sidebar__logo { font-size: 28px; }
    .sidebar__title {
      font-size: 20px;
      font-weight: 700;
      letter-spacing: -0.5px;
    }
    .sidebar__nav {
      list-style: none;
      padding: 12px 0;
      margin: 0;
      flex: 1;
    }
    .sidebar__nav li a {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 20px;
      color: rgba(255,255,255,0.7);
      text-decoration: none;
      font-size: 15px;
      font-weight: 500;
      transition: all 0.2s;
      border-left: 3px solid transparent;
    }
    .sidebar__nav li a:hover {
      background: rgba(255,255,255,0.08);
      color: white;
    }
    .sidebar__nav li a.active {
      background: rgba(255,255,255,0.12);
      color: white;
      border-left-color: #34d399;
    }
    .nav-icon { font-size: 18px; width: 20px; text-align: center; }
    .sidebar__footer {
      padding: 16px 20px;
      border-top: 1px solid rgba(255,255,255,0.1);
      color: rgba(255,255,255,0.4);
      text-align: center;
    }
  `]
})
export class SidebarComponent {}
