import { apiSlice } from "./mainApiSlice";
import { ENDPOINTS } from "../constants";
import { TeamMember, Brand } from "../models/entities";

export interface TeamApiResponse {
	count: number;
	next: string | null;
	previous: string | null;
	results: TeamMember[];
}

export interface BrandsApiResponse {
	count: number;
	next: string | null;
	previous: string | null;
	results: Brand[];
}

export const aboutSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getTeamMembers: builder.query<TeamApiResponse, void>({
			query: () => `${ENDPOINTS.TEAM_MEMBERS}/`,
		}),
		getBrands: builder.query<BrandsApiResponse, void>({
			query: () => `${ENDPOINTS.BRANDS}/`,
		}),
	}),
});

export const { useGetTeamMembersQuery, useGetBrandsQuery } = aboutSlice;
