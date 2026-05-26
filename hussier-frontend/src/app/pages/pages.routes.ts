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
import { adminGuard, huissierGuard, clercGuard } from 'src/services/role.guard';
import { ProfilComponent } from './profil/profil.component';
import { RolesComponent } from './roles/roles.component';

export default [
    { path: 'profil', component: ProfilComponent },
    { path: 'roles', component: RolesComponent },
    { path: 'dossier', component: DossierComponent, canActivate: [clercGuard] },
    { path: 'client', component: ClientComponent, canActivate: [clercGuard] },
    { path: 'partie', component: PartieComponent, canActivate: [clercGuard] },
    { path: 'paiement', component: PaiementComponent, canActivate: [huissierGuard] },
    { path: 'acte', component: ActeComponent, canActivate: [clercGuard] },
    { path: 'affectation', component: AffectationComponent, canActivate: [huissierGuard] },
    { path: 'document', component: DocumentComponent, canActivate: [clercGuard] },
    { path: 'archive', component: ArchiveComponent, canActivate: [huissierGuard] },
    { path: 'agenda', component: AgendaComponent, canActivate: [clercGuard] },
    { path: 'cabinet', component: CabinetComponent, canActivate: [adminGuard] },
    { path: 'utilisateur', component: UtilisateurComponent, canActivate: [adminGuard] },
    { path: 'audit', component: AuditComponent, canActivate: [adminGuard] },
    { path: 'documentation', component: Documentation },
    { path: 'crud', component: Crud },
    { path: 'empty', component: Empty },
    { path: '**', redirectTo: '/notfound' }
] as Routes;
