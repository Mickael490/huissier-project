import { Routes } from '@angular/router';
import { DocumentComponent } from './document.component/document.component';
import { Documentation } from './documentation/documentation';
import { Crud } from './crud/crud';
import { Empty } from './empty/empty';
import { CabinetComponent } from './cabinet-component/cabinet-component';
import { ActeComponent } from './acte.component/acte.component';
import { PartieComponent } from './partie.component/partie.component';
import { ClientComponent } from './client.component/client.component';
import { AgendaComponent } from './agenda.component/agenda.component';
import { ArchiveComponent } from './archive.component/archive.component';
import { AuditComponent } from './audit.component/audit.component';
import { UtilisateurComponent } from './utilisateur.component/utilisateur.component';
import { DossierComponent } from './dossier.component/dossier.component';
import { AffectationComponent } from './affectation.component/affectation.component';
import { PaiementComponent } from './paiement.component/paiement.component';
import {
    adminGuard,
    dossierGuard,
    clientGuard,
    partieGuard,
    acteGuard,
    paiementGuard,
    affectationGuard,
    documentGuard,
    archiveGuard,
    agendaGuard
} from 'src/services/role.guard';
import { ProfilComponent } from './profil/profil.component';
import { RolesComponent } from './roles/roles.component';

export default [
    { path: 'profil', component: ProfilComponent },
    { path: 'roles', component: RolesComponent, canActivate: [adminGuard] },
    { path: 'dossier', component: DossierComponent, canActivate: [dossierGuard] },
    { path: 'client', component: ClientComponent, canActivate: [clientGuard] },
    { path: 'partie', component: PartieComponent, canActivate: [partieGuard] },
    { path: 'paiement', component: PaiementComponent, canActivate: [paiementGuard] },
    { path: 'acte', component: ActeComponent, canActivate: [acteGuard] },
    { path: 'affectation', component: AffectationComponent, canActivate: [affectationGuard] },
    { path: 'document', component: DocumentComponent, canActivate: [documentGuard] },
    { path: 'archive', component: ArchiveComponent, canActivate: [archiveGuard] },
    { path: 'agenda', component: AgendaComponent, canActivate: [agendaGuard] },
    { path: 'cabinet', component: CabinetComponent, canActivate: [adminGuard] },
    { path: 'utilisateur', component: UtilisateurComponent, canActivate: [adminGuard] },
    { path: 'audit', component: AuditComponent, canActivate: [adminGuard] },
    { path: 'documentation', component: Documentation },
    { path: 'crud', component: Crud },
    { path: 'empty', component: Empty },
    { path: '**', redirectTo: '/notfound' }
] as Routes;
