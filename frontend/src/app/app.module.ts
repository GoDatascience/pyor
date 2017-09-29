import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms'
import {MdAutocompleteModule, MdButtonModule, MdCheckboxModule, MdDatepickerModule, MdIconModule, MdInputModule, MdNativeDateModule, MdSelectModule, MdToolbarModule, MdTooltipModule} from '@angular/material';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {AppComponent} from './app.component';
import {RouterModule, Routes} from "@angular/router";
import {MRQDashboardComponent} from './mrq-dashboard/mrq-dashboard.component';
import {AddTaskComponent} from './add-task/add-task.component';
import {AddJobComponent} from './add-job/add-job.component';
import {MultiFileSelectorComponent} from './multi-file-selector/multi-file-selector.component';
import {InputFileComponent} from "./input-file/input-file.component";
import {HttpClientModule} from '@angular/common/http';
import {HttpModule} from "@angular/http";
import {InfoDialogComponent} from './info-dialog/info-dialog.component';
import {InfoDialogService} from "./info-dialog/info-dialog.service";

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
    AddJobComponent,
    MultiFileSelectorComponent,
    InputFileComponent,
    InfoDialogComponent
  ],
  entryComponents: [InfoDialogComponent],
  imports: [
    BrowserModule,
    MdToolbarModule,
    MdButtonModule,
    MdInputModule,
    BrowserAnimationsModule,
    MdSelectModule,
    MdIconModule,
    MdTooltipModule,
    MdAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpModule,
    MdCheckboxModule,
    MdDatepickerModule,
    MdNativeDateModule,
    RouterModule.forRoot(appRoutes),
  ],
  exports: [
    MdToolbarModule,
    MdButtonModule,
    MdInputModule,
    BrowserAnimationsModule,
    MdSelectModule,
    MdTooltipModule,
    MdIconModule,
    MdAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
    MdCheckboxModule,
    MdDatepickerModule,
    MdNativeDateModule
  ],
  providers: [InfoDialogService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
