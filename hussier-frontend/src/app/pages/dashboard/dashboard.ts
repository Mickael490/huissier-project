import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartModule } from 'primeng/chart';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { BadgeModule } from 'primeng/badge';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { RouterModule } from '@angular/router';
import { hasRole, AppRole } from 'src/services/role.guard';

@Component({
    selector: 'app-dashboard',
    standalone: true,
    imports: [CommonModule, ChartModule, TableModule, TagModule, ButtonModule, DialogModule, BadgeModule, RouterModule],
    template: `
    <div style="display:flex; flex-direction:column; gap:20px;">

      <!-- HEADER AVEC NOTIFICATIONS -->
      <div style="background:linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 60%, #4f46e5 100%); border-radius:16px; padding:24px 32px; color:white; box-shadow:0 4px 20px rgba(30,58,95,0.3);">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-size:12px; color:rgba(255,255,255,0.6); margin-bottom:4px; letter-spacing:2px; text-transform:uppercase;">Cabinet Me SAWADOGO — Huissier de Justice</div>
            <div style="font-size:24px; font-weight:700; margin-bottom:4px;">Bonjour, {{ nomUtilisateur }} 👋</div>
            <div style="font-size:13px; color:rgba(255,255,255,0.7);">{{ heureActuelle }} · {{ dateAujourdhui }}</div>
          </div>
          <div style="display:flex; align-items:center; gap:16px;">

            <!-- Météo cabinet -->
            <div style="background:rgba(255,255,255,0.12); border-radius:12px; padding:12px 20px; text-align:center; backdrop-filter:blur(8px);">
              <div style="font-size:11px; color:rgba(255,255,255,0.6); margin-bottom:4px;">Taux de cloture</div>
              <div style="font-size:22px; font-weight:800;">{{ tauxCloture }}%</div>
              <div style="font-size:10px; color:rgba(255,255,255,0.6);">ce mois</div>
            </div>

            <!-- Cloche notifications -->
            <div style="position:relative; cursor:pointer;" (click)="notifDialog = true">
              <div style="width:48px; height:48px; border-radius:12px; background:rgba(255,255,255,0.15); display:flex; align-items:center; justify-content:center; backdrop-filter:blur(8px);">
                <i class="pi pi-bell" style="font-size:20px; color:white;"></i>
              </div>
              <span *ngIf="dossiersUrgents.length > 0"
                style="position:absolute; top:-6px; right:-6px; background:#ef4444; color:white; border-radius:50%; width:20px; height:20px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; border:2px solid #1e3a5f;">
                {{ dossiersUrgents.length }}
              </span>
            </div>

            <!-- Rôle -->
            <div style="background:rgba(255,255,255,0.12); border-radius:12px; padding:12px 20px; backdrop-filter:blur(8px);">
              <div style="font-size:11px; color:rgba(255,255,255,0.6); margin-bottom:2px;">Connecte en tant que</div>
              <div style="font-size:15px; font-weight:700; text-transform:uppercase; letter-spacing:1px;">{{ roleUtilisateur }}</div>
            </div>
          </div>
        </div>

        <!-- Barre progression objectif mensuel -->
        <div *ngIf="canFinance" style="margin-top:20px; background:rgba(255,255,255,0.1); border-radius:10px; padding:14px 20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:12px; color:rgba(255,255,255,0.8); font-weight:600;">Objectif mensuel — {{ (stats?.kpis?.paiements_mois || 0) | number:'1.0-0' }} FCFA encaisses</span>
            <span style="font-size:12px; color:rgba(255,255,255,0.8);">{{ progressionMois }}%</span>
          </div>
          <div style="background:rgba(255,255,255,0.2); border-radius:6px; height:8px; overflow:hidden;">
            <div [style]="'height:100%; border-radius:6px; background:linear-gradient(90deg, #10b981, #4ade80); width:' + progressionMois + '%; transition:width 1s ease;'"></div>
          </div>
        </div>
      </div>

      <!-- ACTIONS RAPIDES (adaptees au role) -->
      <div style="background:white; border-radius:14px; padding:18px 20px; box-shadow:0 1px 4px rgba(0,0,0,0.08);">
        <div style="font-size:13px; font-weight:700; color:#1e3a5f; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
          <i class="pi pi-bolt" style="color:#f59e0b;"></i> Actions rapides
        </div>
        <div style="display:flex; gap:12px; flex-wrap:wrap;">
          <a *ngFor="let qa of quickActions" [routerLink]="qa.link"
            style="display:flex; align-items:center; gap:10px; padding:10px 16px; border-radius:10px; text-decoration:none; background:#f8fafc; border:1px solid #f1f5f9; transition:all .15s;"
            onmouseover="this.style.background='#eef2ff'" onmouseout="this.style.background='#f8fafc'">
            <div [style]="'width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; background:' + qa.color + '1a;'">
              <i [class]="qa.icon" [style]="'color:' + qa.color + '; font-size:14px;'"></i>
            </div>
            <span style="font-size:13px; font-weight:600; color:#334155;">{{ qa.label }}</span>
          </a>
        </div>
      </div>

      <!-- ALERTES URGENTES -->
      <div *ngIf="dossiersUrgents.length > 0" style="background:linear-gradient(135deg, #fef2f2, #fff5f5); border:1px solid #fecaca; border-radius:14px; padding:16px 20px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
          <div style="width:36px; height:36px; border-radius:10px; background:#ef4444; display:flex; align-items:center; justify-content:center;">
            <i class="pi pi-exclamation-triangle" style="color:white; font-size:16px;"></i>
          </div>
          <div>
            <div style="font-size:15px; font-weight:700; color:#b91c1c;">{{ dossiersUrgents.length }} dossier(s) avec delai critique</div>
            <div style="font-size:12px; color:#ef4444;">Echeance dans moins de 7 jours</div>
          </div>
        </div>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
          <div *ngFor="let d of dossiersUrgents.slice(0,4)"
            style="background:white; border:1px solid #fecaca; border-radius:10px; padding:10px 14px; display:flex; align-items:center; gap:10px;">
            <div style="width:8px; height:8px; border-radius:50%; background:#ef4444; animation:pulse 1s infinite;"></div>
            <div>
              <div style="font-weight:700; color:#1e293b; font-size:13px;">{{ d.numero }}</div>
              <div style="font-size:11px; color:#ef4444;">{{ d.jours_restants }} jour(s) restant(s)</div>
            </div>
          </div>
        </div>
      </div>

      <!-- KPIs PRINCIPAUX -->
      <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px;">

        <div style="background:linear-gradient(135deg, #f0f4ff 0%, #f5f3ff 100%); border-radius:14px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); border-left:4px solid #4f46e5;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
            <div>
              <div style="font-size:12px; color:#94a3b8; margin-bottom:4px; text-transform:uppercase; letter-spacing:1px;">Dossiers</div>
              <div style="font-size:32px; font-weight:800; color:#4f46e5; line-height:1;">{{ stats?.kpis?.total_dossiers || 0 }}</div>
            </div>
            <div style="width:48px; height:48px; border-radius:12px; background:#ede9fe; display:flex; align-items:center; justify-content:center;">
              <i class="pi pi-folder" style="color:#4f46e5; font-size:20px;"></i>
            </div>
          </div>
          <div style="display:flex; gap:8px; margin-bottom:10px;">
            <span style="background:#dcfce7; color:#16a34a; padding:3px 8px; border-radius:20px; font-size:11px; font-weight:600;">{{ stats?.kpis?.dossiers_actifs || 0 }} actifs</span>
            <span style="background:#fef3c7; color:#d97706; padding:3px 8px; border-radius:20px; font-size:11px; font-weight:600;">{{ stats?.kpis?.dossiers_nouveaux || 0 }} nouveaux</span>
          </div>
          <!-- Mini sparkline simulé -->
          <div style="display:flex; align-items:flex-end; gap:3px; height:28px;">
            <div *ngFor="let h of sparkDossiers" [style]="'background:#4f46e5; opacity:0.3; border-radius:3px; width:100%; height:' + h + '%'"></div>
          </div>
        </div>

        <div *ngIf="canFinance" style="background:white; border-radius:14px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); border-left:4px solid #10b981;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
            <div>
              <div style="font-size:12px; color:#94a3b8; margin-bottom:4px; text-transform:uppercase; letter-spacing:1px;">Encaissements</div>
              <div style="font-size:26px; font-weight:800; color:#10b981; line-height:1;">{{ (stats?.kpis?.paiements_mois || 0) | number:'1.0-0' }}</div>
              <div style="font-size:11px; color:#94a3b8;">FCFA ce mois</div>
            </div>
            <div style="width:48px; height:48px; border-radius:12px; background:#d1fae5; display:flex; align-items:center; justify-content:center;">
              <i class="pi pi-dollar" style="color:#10b981; font-size:20px;"></i>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:6px;">
            <i class="pi pi-arrow-up-right" style="color:#10b981; font-size:12px;"></i>
            <span style="font-size:12px; color:#10b981; font-weight:600;">+{{ evolutionPaiements }}% vs mois precedent</span>
          </div>
        </div>

        <div *ngIf="canClients" style="background:white; border-radius:14px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); border-left:4px solid #f97316;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
            <div>
              <div style="font-size:12px; color:#94a3b8; margin-bottom:4px; text-transform:uppercase; letter-spacing:1px;">Clients</div>
              <div style="font-size:32px; font-weight:800; color:#f97316; line-height:1;">{{ stats?.kpis?.total_clients || 0 }}</div>
            </div>
            <div style="width:48px; height:48px; border-radius:12px; background:#fff7ed; display:flex; align-items:center; justify-content:center;">
              <i class="pi pi-users" style="color:#f97316; font-size:20px;"></i>
            </div>
          </div>
          <div style="display:flex; align-items:flex-end; gap:3px; height:28px;">
            <div *ngFor="let h of sparkClients" [style]="'background:#f97316; opacity:0.3; border-radius:3px; width:100%; height:' + h + '%'"></div>
          </div>
        </div>

        <div style="background:white; border-radius:14px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); border-left:4px solid #06b6d4;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
            <div>
              <div style="font-size:12px; color:#94a3b8; margin-bottom:4px; text-transform:uppercase; letter-spacing:1px;">RDV aujourd'hui</div>
              <div style="font-size:32px; font-weight:800; color:#06b6d4; line-height:1;">{{ rdvAujourdhui }}</div>
            </div>
            <div style="width:48px; height:48px; border-radius:12px; background:#cffafe; display:flex; align-items:center; justify-content:center;">
              <i class="pi pi-calendar" style="color:#06b6d4; font-size:20px;"></i>
            </div>
          </div>
          <div style="font-size:12px; color:#94a3b8;">{{ stats?.kpis?.rdv_semaine || 0 }} cette semaine</div>
        </div>

      </div>

      <!-- KPIs SECONDAIRES -->
      <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px;">
        <div *ngIf="canActes" style="background:white; border-radius:12px; padding:16px 20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); display:flex; align-items:center; gap:14px;">
          <div style="width:40px; height:40px; border-radius:10px; background:#ede9fe; display:flex; align-items:center; justify-content:center;">
            <i class="pi pi-file-edit" style="color:#8b5cf6; font-size:16px;"></i>
          </div>
          <div>
            <div style="font-size:20px; font-weight:700; color:#1e293b;">{{ stats?.kpis?.total_actes || 0 }}</div>
            <div style="font-size:12px; color:#94a3b8;">Actes</div>
          </div>
        </div>
        <div *ngIf="canActes" style="background:white; border-radius:12px; padding:16px 20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); display:flex; align-items:center; gap:14px;">
          <div style="width:40px; height:40px; border-radius:10px; background:#fef2f2; display:flex; align-items:center; justify-content:center;">
            <i class="pi pi-sitemap" style="color:#ef4444; font-size:16px;"></i>
          </div>
          <div>
            <div style="font-size:20px; font-weight:700; color:#1e293b;">{{ stats?.kpis?.total_parties || 0 }}</div>
            <div style="font-size:12px; color:#94a3b8;">Parties</div>
          </div>
        </div>
        <div *ngIf="canDossiers" style="background:white; border-radius:12px; padding:16px 20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); display:flex; align-items:center; gap:14px;">
          <div style="width:40px; height:40px; border-radius:10px; background:#f0fdf4; display:flex; align-items:center; justify-content:center;">
            <i class="pi pi-file" style="color:#10b981; font-size:16px;"></i>
          </div>
          <div>
            <div style="font-size:20px; font-weight:700; color:#1e293b;">{{ stats?.kpis?.total_documents || 0 }}</div>
            <div style="font-size:12px; color:#94a3b8;">Documents</div>
          </div>
        </div>
        <div *ngIf="canFinance" style="background:white; border-radius:12px; padding:16px 20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); display:flex; align-items:center; gap:14px;">
          <div style="width:40px; height:40px; border-radius:10px; background:#fff7ed; display:flex; align-items:center; justify-content:center;">
            <i class="pi pi-inbox" style="color:#f97316; font-size:16px;"></i>
          </div>
          <div>
            <div style="font-size:20px; font-weight:700; color:#1e293b;">{{ stats?.kpis?.total_archives || 0 }}</div>
            <div style="font-size:12px; color:#94a3b8;">Archives</div>
          </div>
        </div>
      </div>

      <!-- GRAPHIQUES -->
      <div style="display:grid; grid-template-columns:5fr 7fr; gap:16px;">
        <div style="background:white; border-radius:14px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.08);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <div>
              <div style="font-size:15px; font-weight:700; color:#1e3a5f;">Repartition par type</div>
              <div style="font-size:12px; color:#94a3b8;">Types d'affaires traites</div>
            </div>
            <span style="background:#ede9fe; color:#4f46e5; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600;">{{ stats?.kpis?.total_dossiers || 0 }} total</span>
          </div>
          <div *ngIf="chartType?.labels?.length > 0">
            <p-chart type="doughnut" [data]="chartType" [options]="doughnutOptions" style="height:220px"></p-chart>
          </div>
          <div *ngIf="!chartType?.labels?.length" style="height:220px; display:flex; align-items:center; justify-content:center; flex-direction:column; color:#94a3b8;">
            <i class="pi pi-chart-pie" style="font-size:36px; margin-bottom:8px;"></i>
            <span>Aucune donnee</span>
          </div>
        </div>

        <div style="background:white; border-radius:14px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.08);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <div>
              <div style="font-size:15px; font-weight:700; color:#1e3a5f;">Dossiers par statut</div>
              <div style="font-size:12px; color:#94a3b8;">Vue d'ensemble operationnelle</div>
            </div>
          </div>
          <div *ngIf="chartStatut?.labels?.length > 0">
            <p-chart type="bar" [data]="chartStatut" [options]="barOptions" style="height:220px"></p-chart>
          </div>
          <div *ngIf="!chartStatut?.labels?.length" style="height:220px; display:flex; align-items:center; justify-content:center; flex-direction:column; color:#94a3b8;">
            <i class="pi pi-chart-bar" style="font-size:36px; margin-bottom:8px;"></i>
            <span>Aucune donnee</span>
          </div>
        </div>
      </div>

      <!-- COMPARATIF MOIS -->
      <div style="background:white; border-radius:14px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.08);">
        <div style="font-size:15px; font-weight:700; color:#1e3a5f; margin-bottom:16px;">Comparatif mois en cours vs mois precedent</div>
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px;">
          <div *ngFor="let item of comparatif" style="background:#f8fafc; border-radius:10px; padding:16px;">
            <div style="font-size:12px; color:#94a3b8; margin-bottom:8px;">{{ item.label }}</div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span style="font-size:20px; font-weight:800; color:#1e293b;">{{ item.actuel }}</span>
              <i [class]="item.hausse ? 'pi pi-arrow-up-right' : 'pi pi-arrow-down-right'"
                [style]="'font-size:14px; color:' + (item.hausse ? '#10b981' : '#ef4444')"></i>
            </div>
            <div style="font-size:12px; color:#94a3b8;">Precedent : {{ item.precedent }}</div>
            <div style="margin-top:8px; background:#e2e8f0; border-radius:4px; height:4px; overflow:hidden;">
              <div [style]="'height:100%; border-radius:4px; background:' + (item.hausse ? '#10b981' : '#ef4444') + '; width:' + item.pct + '%'"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- HEAT MAP ACTIVITE + TIMELINE -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">

        <!-- Heat map activite par jour -->
        <div style="background:white; border-radius:14px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.08);">
          <div style="font-size:15px; font-weight:700; color:#1e3a5f; margin-bottom:4px;">Activite par jour de la semaine</div>
          <div style="font-size:12px; color:#94a3b8; margin-bottom:16px;">Intensite des actions sur 4 semaines</div>
          <div style="display:flex; gap:8px; margin-bottom:8px;">
            <div *ngFor="let jour of jours" style="flex:1; text-align:center; font-size:11px; color:#94a3b8; font-weight:600;">{{ jour }}</div>
          </div>
          <div *ngFor="let semaine of heatmap" style="display:flex; gap:8px; margin-bottom:6px;">
            <div *ngFor="let val of semaine"
              [style]="'flex:1; height:32px; border-radius:6px; background:' + getHeatColor(val) + '; display:flex; align-items:center; justify-content:center;'"
              [title]="val + ' actions'">
              <span *ngIf="val > 0" style="font-size:10px; font-weight:700; color:white;">{{ val }}</span>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:8px; margin-top:12px;">
            <span style="font-size:11px; color:#94a3b8;">Moins</span>
            <div *ngFor="let c of ['#e2e8f0','#bfdbfe','#93c5fd','#3b82f6','#1d4ed8']"
              [style]="'width:20px; height:12px; border-radius:3px; background:' + c"></div>
            <span style="font-size:11px; color:#94a3b8;">Plus</span>
          </div>
        </div>

        <!-- Timeline dernières actions -->
        <div style="background:white; border-radius:14px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.08); overflow-y:auto; max-height:350px;">
          <div style="font-size:15px; font-weight:700; color:#1e3a5f; margin-bottom:4px;">Dernieres actions</div>
          <div style="font-size:12px; color:#94a3b8; margin-bottom:16px;">Feed en temps reel</div>
          <div style="position:relative;">
            <div style="position:absolute; left:19px; top:0; bottom:0; width:2px; background:#e2e8f0;"></div>
            <div *ngFor="let action of dernieresActions" style="display:flex; gap:14px; margin-bottom:16px; position:relative;">
              <div [style]="'width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; z-index:1; background:' + getActionBg(action.type)">
                <i [class]="getActionIcon(action.type)" [style]="'font-size:14px; color:' + getActionColor(action.type)"></i>
              </div>
              <div style="flex:1; padding-top:8px;">
                <div style="font-size:13px; font-weight:600; color:#1e293b;">{{ action.texte }}</div>
                <div style="font-size:11px; color:#94a3b8; margin-top:2px;">{{ action.temps }}</div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- TABLES FINALES -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">

        <!-- Dossiers récents -->
        <div style="background:white; border-radius:14px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.08);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <div>
              <div style="font-size:15px; font-weight:700; color:#1e3a5f;">Dossiers recents</div>
              <div style="font-size:12px; color:#94a3b8;">Derniers ouverts</div>
            </div>
            <a routerLink="/pages/dossier" style="color:#4f46e5; font-size:12px; font-weight:600; text-decoration:none;">Voir tout →</a>
          </div>
          <p-table [value]="stats?.derniers_dossiers || []">
            <ng-template #header>
              <tr style="background:#f8fafc;">
                <th style="padding:10px; font-size:11px; color:#1e3a5f; font-weight:700;">NUMERO</th>
                <th style="padding:10px; font-size:11px; color:#1e3a5f; font-weight:700;">OBJET</th>
                <th style="padding:10px; font-size:11px; color:#1e3a5f; font-weight:700;">STATUT</th>
              </tr>
            </ng-template>
            <ng-template #body let-d>
              <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px; font-weight:700; color:#4f46e5; font-size:12px;">{{ d.numero }}</td>
                <td style="padding:10px; font-size:12px; color:#475569;">{{ d.objet }}</td>
                <td style="padding:10px;"><p-tag [value]="d.statut" [severity]="getStatutSeverity(d.statut)"></p-tag></td>
              </tr>
            </ng-template>
            <ng-template #emptymessage>
              <tr><td colspan="3" style="text-align:center; padding:24px; color:#94a3b8;">Aucun dossier recent</td></tr>
            </ng-template>
          </p-table>
        </div>

        <!-- Prochains RDV -->
        <div style="background:white; border-radius:14px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.08);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <div>
              <div style="font-size:15px; font-weight:700; color:#1e3a5f;">Prochains rendez-vous</div>
              <div style="font-size:12px; color:#94a3b8;">Agenda de la semaine</div>
            </div>
            <a routerLink="/pages/agenda" style="color:#4f46e5; font-size:12px; font-weight:600; text-decoration:none;">Voir tout →</a>
          </div>
          <div style="display:flex; flex-direction:column; gap:10px;">
            <div *ngFor="let rdv of stats?.prochains_rdv || []"
              style="display:flex; align-items:center; gap:12px; padding:12px; background:#f8fafc; border-radius:10px; border-left:3px solid #8b5cf6;">
              <div style="width:36px; height:36px; border-radius:10px; background:#ede9fe; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <i class="pi pi-calendar" style="color:#8b5cf6; font-size:14px;"></i>
              </div>
              <div style="flex:1; min-width:0;">
                <div style="font-weight:700; color:#1e293b; font-size:13px;">{{ rdv.titre }}</div>
                <div style="font-size:11px; color:#94a3b8; margin-top:2px;">{{ rdv.date_debut | date:"dd/MM HH:mm" }} · {{ rdv.lieu || "—" }}</div>
              </div>
            </div>
            <div *ngIf="!stats?.prochains_rdv?.length" style="text-align:center; padding:24px; color:#94a3b8;">Aucun RDV a venir</div>
          </div>
        </div>

      </div>

      <!-- DERNIERS PAIEMENTS -->
      <div *ngIf="canFinance" style="background:white; border-radius:14px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.08);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <div>
            <div style="font-size:15px; font-weight:700; color:#1e3a5f;">Derniers paiements</div>
            <div style="font-size:12px; color:#94a3b8;">Encaissements recents</div>
          </div>
          <a routerLink="/pages/paiement" style="color:#4f46e5; font-size:12px; font-weight:600; text-decoration:none;">Voir tout →</a>
        </div>
        <p-table [value]="stats?.derniers_paiements || []">
          <ng-template #header>
            <tr style="background:#f8fafc;">
              <th style="padding:10px; font-size:11px; color:#1e3a5f; font-weight:700;">TYPE</th>
              <th style="padding:10px; font-size:11px; color:#1e3a5f; font-weight:700;">MONTANT (FCFA)</th>
              <th style="padding:10px; font-size:11px; color:#1e3a5f; font-weight:700;">MODE</th>
              <th style="padding:10px; font-size:11px; color:#1e3a5f; font-weight:700;">DATE</th>
            </tr>
          </ng-template>
          <ng-template #body let-p>
            <tr style="border-bottom:1px solid #f1f5f9;">
              <td style="padding:10px; font-size:12px; color:#475569;">{{ p.type }}</td>
              <td style="padding:10px; font-size:15px; font-weight:800; color:#10b981;">{{ p.montant | number:"1.0-0" }}</td>
              <td style="padding:10px;">
                <span style="padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; background:#ede9fe; color:#4f46e5;">{{ p.mode }}</span>
              </td>
              <td style="padding:10px; font-size:12px; color:#64748b;">{{ p.date | date:"dd/MM/yyyy" }}</td>
            </tr>
          </ng-template>
          <ng-template #emptymessage>
            <tr><td colspan="4" style="text-align:center; padding:24px; color:#94a3b8;">Aucun paiement recent</td></tr>
          </ng-template>
        </p-table>
      </div>

    </div>

    <!-- DIALOG NOTIFICATIONS -->
    <p-dialog [(visible)]="notifDialog" header="Alertes et notifications" [modal]="true" [style]="{width:'500px'}">
      <div *ngIf="dossiersUrgents.length === 0" style="text-align:center; padding:30px; color:#94a3b8;">
        <i class="pi pi-check-circle" style="font-size:36px; display:block; margin-bottom:8px; color:#10b981;"></i>
        Aucune alerte urgente
      </div>
      <div *ngFor="let d of dossiersUrgents" style="display:flex; align-items:center; gap:14px; padding:14px; border-radius:10px; border:1px solid #fecaca; background:#fef2f2; margin-bottom:10px;">
        <div style="width:40px; height:40px; border-radius:10px; background:#ef4444; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <i class="pi pi-exclamation-triangle" style="color:white; font-size:16px;"></i>
        </div>
        <div>
          <div style="font-weight:700; color:#1e293b; font-size:14px;">{{ d.numero }}</div>
          <div style="font-size:12px; color:#ef4444; font-weight:600;">Echeance dans {{ d.jours_restants }} jour(s)</div>
          <div style="font-size:12px; color:#94a3b8;">{{ d.objet }}</div>
        </div>
      </div>
      <ng-template pTemplate="footer">
        <p-button label="Fermer" icon="pi pi-times" text (click)="notifDialog = false" />
        <p-button label="Voir tous les dossiers" icon="pi pi-folder" routerLink="/pages/dossier" (click)="notifDialog = false" />
      </ng-template>
    </p-dialog>
    `
})
export class Dashboard implements OnInit, OnDestroy {
    stats: any = null;
    chartType: any = {};
    chartStatut: any = {};
    doughnutOptions: any = {};
    barOptions: any = {};
    nomUtilisateur: string = '';
    roleUtilisateur: string = '';
    dateAujourdhui: string = '';
    heureActuelle: string = '';
    notifDialog = false;
    dossiersUrgents: any[] = [];
    rdvAujourdhui = 0;
    tauxCloture = 0;
    progressionMois = 0;
    evolutionPaiements = 12;
    private timer: any;

    sparkDossiers = [30,50,40,70,60,80,100];
    sparkClients = [60,40,80,50,90,70,100];

    jours = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'];
    heatmap: number[][] = [];

    comparatif: any[] = [];

    dernieresActions: any[] = [
      { type: 'CREATE', texte: 'Nouveau dossier DOS-2026-0005 cree', temps: 'Il y a 5 min' },
      { type: 'UPDATE', texte: 'Client Sawadogo Jean modifie', temps: 'Il y a 23 min' },
      { type: 'PAYMENT', texte: 'Paiement 150 000 FCFA encaisse', temps: 'Il y a 1h' },
      { type: 'DOCUMENT', texte: 'Document acte_signification.pdf uploade', temps: 'Il y a 2h' },
      { type: 'AGENDA', texte: 'RDV Audience planifie demain 9h00', temps: 'Il y a 3h' },
      { type: 'LOGIN', texte: 'Connexion depuis Ouagadougou', temps: 'Il y a 4h' },
    ];

    // --- Visibilite par role (aligne sur role.guard.ts) ---
    get isAdmin(): boolean { return hasRole(['ADMIN']); }
    get canFinance(): boolean { return hasRole(['ADMIN', 'HUISSIER']); }          // Paiements, Affectations, Archives
    get canActes(): boolean { return hasRole(['ADMIN', 'HUISSIER', 'CLERC']); }     // Parties, Actes
    get canClients(): boolean { return hasRole(['ADMIN', 'HUISSIER', 'CLERC', 'SECRETAIRE']); }
    get canDossiers(): boolean { return hasRole(['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT']); }

    // Actions rapides specifiques au profil connecte
    quickActions: { label: string; icon: string; color: string; link: string }[] = [];

    constructor(private http: HttpClient) {}

    private buildQuickActions() {
        const a: any[] = [];
        if (this.canDossiers) a.push({ label: 'Nouveau dossier', icon: 'pi pi-folder-plus', color: '#4f46e5', link: '/pages/dossier' });
        if (this.canActes) a.push({ label: 'Rediger un acte', icon: 'pi pi-file-edit', color: '#8b5cf6', link: '/pages/acte' });
        if (this.canClients) a.push({ label: 'Ajouter un client', icon: 'pi pi-user-plus', color: '#f97316', link: '/pages/client' });
        if (this.canFinance) a.push({ label: 'Enregistrer un paiement', icon: 'pi pi-dollar', color: '#10b981', link: '/pages/paiement' });
        a.push({ label: 'Planifier un RDV', icon: 'pi pi-calendar-plus', color: '#06b6d4', link: '/pages/agenda' });
        if (this.canDossiers) a.push({ label: 'Importer un document', icon: 'pi pi-file', color: '#0ea5e9', link: '/pages/document' });
        if (this.isAdmin) a.push({ label: 'Gerer les utilisateurs', icon: 'pi pi-users', color: '#64748b', link: '/pages/utilisateur' });
        this.quickActions = a;
    }

    ngOnInit() {
        this.nomUtilisateur = (localStorage.getItem('prenom') || '' + ' ' + (localStorage.getItem('nom') || '')).trim() || 'Utilisateur';
        this.roleUtilisateur = localStorage.getItem('role') || '';
        this.dateAujourdhui = new Date().toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        this.updateHeure();
        this.timer = setInterval(() => this.updateHeure(), 1000);
        this.generateHeatmap();
        this.buildQuickActions();
        this.loadStats();
    }

    ngOnDestroy() {
        if (this.timer) clearInterval(this.timer);
    }

    updateHeure() {
        this.heureActuelle = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    generateHeatmap() {
        this.heatmap = Array.from({ length: 4 }, () =>
            Array.from({ length: 7 }, () => Math.floor(Math.random() * 15))
        );
    }

    getHeatColor(val: number): string {
        if (val === 0) return '#e2e8f0';
        if (val < 4) return '#bfdbfe';
        if (val < 8) return '#93c5fd';
        if (val < 12) return '#3b82f6';
        return '#1d4ed8';
    }

    loadStats() {
        const token = localStorage.getItem('token');
        const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
        this.http.get<any>(`${environment.apiUrl}/statistics/dashboard`, { headers }).subscribe({
            next: (data) => {
                this.stats = data;
                this.buildCharts(data);
                this.buildComparatif(data);
                this.calculateKpis(data);
                this.simulateDossiersUrgents(data);
            },
            error: () => {}
        });
    }

    calculateKpis(data: any) {
        const total = data?.kpis?.total_dossiers || 0;
        const termines = data?.kpis?.dossiers_termines || 0;
        this.tauxCloture = total > 0 ? Math.round((termines / total) * 100) : 0;
        const objectifMensuel = 500000;
        const paiements = data?.kpis?.paiements_mois || 0;
        this.progressionMois = Math.min(100, Math.round((paiements / objectifMensuel) * 100));
        this.rdvAujourdhui = data?.kpis?.rdv_aujourd_hui || data?.kpis?.rdv_semaine || 0;
    }

    simulateDossiersUrgents(data: any) {
        const dossiers = data?.derniers_dossiers || [];
        this.dossiersUrgents = dossiers.slice(0, 2).map((d: any, i: number) => ({
            ...d,
            jours_restants: 3 + i * 2
        }));
    }

    buildComparatif(data: any) {
        const items: any[] = [
            { label: 'Dossiers', actuel: data?.kpis?.total_dossiers || 0, precedent: Math.max(0, (data?.kpis?.total_dossiers || 0) - 2), hausse: true, pct: 75 },
        ];
        if (this.canClients) items.push({ label: 'Clients', actuel: data?.kpis?.total_clients || 0, precedent: Math.max(0, (data?.kpis?.total_clients || 0) - 1), hausse: true, pct: 80 });
        if (this.canFinance) items.push({ label: 'Paiements (FCFA)', actuel: data?.kpis?.paiements_mois || 0, precedent: Math.max(0, (data?.kpis?.paiements_mois || 0) * 0.88), hausse: true, pct: 88 });
        items.push({ label: 'RDV semaine', actuel: data?.kpis?.rdv_semaine || 0, precedent: Math.max(0, (data?.kpis?.rdv_semaine || 0) - 1), hausse: false, pct: 60 });
        this.comparatif = items;
    }

    buildCharts(data: any) {
        const types = data.graphiques?.dossiers_par_type || [];
        const statuts = data.graphiques?.dossiers_par_statut || [];
        const colors = ['#4f46e5','#10b981','#f97316','#ef4444','#8b5cf6','#06b6d4','#f59e0b','#ec4899'];

        this.chartType = {
            labels: types.map((t: any) => t.type),
            datasets: [{ data: types.map((t: any) => t.count), backgroundColor: colors.slice(0, types.length), borderWidth: 3, borderColor: '#ffffff' }]
        };

        this.chartStatut = {
            labels: statuts.map((s: any) => s.statut),
            datasets: [{ label: 'Dossiers', data: statuts.map((s: any) => s.count), backgroundColor: colors.slice(0, statuts.length), borderRadius: 10, borderSkipped: false }]
        };

        this.doughnutOptions = {
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { padding: 14, font: { size: 11 } } } },
            cutout: '70%'
        };

        this.barOptions = {
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false }, ticks: { font: { size: 11 } } },
                y: { beginAtZero: true, grid: { color: '#f1f5f9' }, ticks: { font: { size: 11 } } }
            }
        };
    }

    getStatutSeverity(statut: string): string {
        switch (statut) {
            case 'nouveau': return 'info';
            case 'en_cours': return 'warning';
            case 'termine': return 'success';
            case 'archive': return 'secondary';
            case 'annule': return 'danger';
            default: return 'info';
        }
    }

    getActionIcon(type: string): string {
        switch (type) {
            case 'CREATE': return 'pi pi-plus';
            case 'UPDATE': return 'pi pi-pencil';
            case 'DELETE': return 'pi pi-trash';
            case 'PAYMENT': return 'pi pi-dollar';
            case 'DOCUMENT': return 'pi pi-file';
            case 'AGENDA': return 'pi pi-calendar';
            case 'LOGIN': return 'pi pi-sign-in';
            default: return 'pi pi-info-circle';
        }
    }

    getActionColor(type: string): string {
        switch (type) {
            case 'CREATE': return '#10b981';
            case 'UPDATE': return '#f97316';
            case 'DELETE': return '#ef4444';
            case 'PAYMENT': return '#4f46e5';
            case 'DOCUMENT': return '#8b5cf6';
            case 'AGENDA': return '#06b6d4';
            case 'LOGIN': return '#3b82f6';
            default: return '#64748b';
        }
    }

    getActionBg(type: string): string {
        switch (type) {
            case 'CREATE': return '#d1fae5';
            case 'UPDATE': return '#fff7ed';
            case 'DELETE': return '#fef2f2';
            case 'PAYMENT': return '#ede9fe';
            case 'DOCUMENT': return '#f3e8ff';
            case 'AGENDA': return '#cffafe';
            case 'LOGIN': return '#dbeafe';
            default: return '#f1f5f9';
        }
    }
}
