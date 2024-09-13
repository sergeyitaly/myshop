import { apiSlice } from "./mainApiSlice";
import { ENDPOINTS } from "../constants";
import { TeamMember, Technology, Brand } from "../models/entities";

export interface TeamApiResponse {
	count: number;
	next: string | null;
	previous: string | null;
	results: TeamMember[];
}

export interface TechnologyApiResponse {
	count: number;
	next: string | null;
	previous: string | null;
	results: Technology[];
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
		getTechnologies: builder.query<TechnologyApiResponse, void>({
			query: () => `${ENDPOINTS.TECHNOLOGIES}/`,
		}),
		getBrands: builder.query<BrandsApiResponse, void>({
			query: () => `${ENDPOINTS.BRANDS}/`,
		}),
	}),
});

export const {
	useGetTeamMembersQuery,
	useGetTechnologiesQuery,
	useGetBrandsQuery,
} = aboutSlice;
