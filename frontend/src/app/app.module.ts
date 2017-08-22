import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {MdButtonModule, MdToolbarModule} from '@angular/material';

import {AppComponent} from './app.component';
import {RouterModule, Routes} from "@angular/router";
import {MRQDashboardComponent} from './mrq-dashboard/mrq-dashboard.component';
import {AddTaskComponent} from './add-task/add-task.component';
import {AddJobComponent} from './add-job/add-job.component';

const appRoutes: Routes = [
  {path: '', redirectTo: '/mrq-dashboard', pathMatch: 'full'},
  {path: 'mrq-dashboard', component: MRQDashboardComponent, pathMatch: 'full'},
  {path: 'add-task', component: AddTaskComponent, pathMatch: 'full'},
  {path: 'add-job', component: AddJobComponent, pathMatch: 'full'}
];


@NgModule({
  declarations: [
    AppComponent,
    MRQDashboardComponent,
    AddTaskComponent,
    AddJobComponent
  ],
  imports: [
    BrowserModule,
    MdToolbarModule,
    MdButtonModule,
    RouterModule.forRoot(appRoutes),
  ],
  exports: [
    MdToolbarModule,
    MdButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
