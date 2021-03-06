import {Injectable} from '@angular/core';
import {Subscription} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {IUser, UsersSearch} from "../../interfaces/interfaces";
import {PeopleService} from "../login/services/people.service";
import {Router} from "@angular/router";
import {FormGroup} from "@angular/forms";
import {environment} from "../../environments/environment";

@Injectable({
    providedIn: 'root'
})
export class SearchStringService {
    private _urlProfiles: string = environment.api_address + "/profile/";
    private _urlAdminPostAccrual: string = environment.api_address + "/admin/accrual/";
    private _urlUserPostAccrual: string = environment.api_address + "/gifts/";
    public foundUsers!: UsersSearch[];

    constructor(
        private _router: Router,
        private _peopleService: PeopleService,
        private _http: HttpClient
    ) {
    }

    public getProfiles(): any {
        return this._http.get<UsersSearch[]>(this._urlProfiles, this._peopleService.optionsForHttp)

    }

    private postAccrualCoins( url: string, body: {}) {
        return this._http.post<any>(url, body, this._peopleService.optionsForHttp)
    };

    public postAdminAccrualCoins(to_profile_id: number[], price: number, comment: string) {
        return this.postAccrualCoins(this._urlAdminPostAccrual,
            {
            "profile_ids": to_profile_id,
            "price": price,
            "comment": comment
        });
    }

    public postUserAccrualCoins(to_profile_id: number[], price: number, comment: string) {
        return this.postAccrualCoins(this._urlUserPostAccrual,
            {
                "destination": to_profile_id,
                "description": comment,
                "accrual": price,
            });
    }
}
