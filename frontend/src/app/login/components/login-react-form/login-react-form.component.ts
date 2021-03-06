import {Component, ElementRef, OnInit, Renderer2, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Router} from "@angular/router";
import {PeopleService} from "../../services/people.service";
import {IUser} from "../../../../interfaces/interfaces";
import {Subscription} from "rxjs";
import {CookieService} from "ngx-cookie-service";

@Component({
    selector: 'app-login-react-form',
    templateUrl: './login-react-form.component.html',
    styleUrls: ['./login-react-form.component.scss']
})
export class LoginReactFormComponent implements OnInit {
    public login: FormGroup = new FormGroup({});
    public activeUser?: Subscription;
    public warning: boolean = false;

    @ViewChild('btn')
    btn!: ElementRef;

    @ViewChild('password')
    password!: ElementRef;


    constructor(
        private _http: HttpClient,
        private _router: Router,
        private _peopleService: PeopleService,
        private _renderer: Renderer2,
        private _cookieService: CookieService,
    ) {
        this._createForm();
    }

    public ngOnInit(): void {
    }


    private _createForm() {
        this.login = new FormGroup({
            email: new FormControl('', [Validators.required]),
            password: new FormControl('', [Validators.required]),
        });
    }

    public changeForm(newValue: any) {
        this.warning = false;
    }

    public onSubmit() {
        const loginEmail = this.login.value.email + "@ussc.ru";
        this._peopleService.postToken(loginEmail, this.login.value.password)
            .subscribe(
                {
                    next: (res: any) => {
                        this._peopleService.token = res?.auth_token;
                        localStorage.setItem('token', this._peopleService.token);
                        this._peopleService.optionsForHttp = {
                            headers: new HttpHeaders({
                                'Content-Type': 'application/json',
                                'Authorization': "Token " + localStorage.getItem('token'),
                            })
                        }
                        this._peopleService.getUserHttp()
                            .subscribe(
                                (user: IUser) => {
                                    if (user) {
                                        if (!user.is_staff) {
                                            localStorage.removeItem('admin');
                                            this._peopleService.findUser.next(user);
                                            this._router.navigate(['main-page', 'merch']);
                                        } else if (user.is_staff) {
                                            localStorage.setItem('admin', 'true');
                                            this._peopleService.findUser.next(user);
                                            this._router.navigate(["admin", "accrual"]);
                                        }
                                    } else {
                                        alert('user not found');
                                    }

                                }, () => {
                                    alert('Something went wrong');
                                });
                        this.login.reset();
                    },

                    error: () => {
                        this.warning = true;
                    }
                });
        // this.activeUser = this._peopleService.getUser(loginEmail, this.login.value.password, this.login);
    }

    public ngAfterViewInit() {
        this._peopleService.showPassword(this.btn.nativeElement, this.password.nativeElement);
    }
}
