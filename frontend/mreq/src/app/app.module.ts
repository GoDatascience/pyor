import {NgModule}      from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {HttpModule} from "@angular/http";
import {RouterModule, Routes} from "@angular/router";

import {FormsModule} from "@angular/forms";
import "hammerjs";

import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {AppComponent}  from './app.component';
import {MaterialModule} from '@angular/material';
import {NavBarComponent}  from './nav-bar/nav-bar.component';


const appRoutes: Routes = [
  {path: '', redirectTo: '/kanban/1', pathMatch: 'full'},
  {path: 'dashboard/', component: NavBarComponent, pathMatch: 'full'},
  {path: 'addTask', component: NavBarComponent, pathMatch: 'full'},
  {path: 'addJob', component: NavBarComponent, pathMatch: 'full'}
];

@NgModule({
  imports: [
    BrowserModule,
    FormsModule ,
    HttpModule,
    MaterialModule,
    BrowserAnimationsModule,
    RouterModule.forRoot(appRoutes),],
  declarations: [AppComponent, NavBarComponent],
  bootstrap: [AppComponent]
})
export class AppModule {
}
