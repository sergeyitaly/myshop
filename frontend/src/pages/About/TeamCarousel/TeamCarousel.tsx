import React from "react";
import { useGetTeamMembersQuery } from "../../../api/aboutSlice";
import { TeamMember } from "../../../models/entities";
import { useTranslation } from "react-i18next";

export const TeamCarousel: React.FC = () => {
	const { data, error, isLoading } = useGetTeamMembersQuery();
	const { t, i18n } = useTranslation();
	const language = i18n.language;

	const teamData = data?.results || [];

	const getTranslatedName = (member: TeamMember): string => {
		return language === "uk"
			? member.name_uk || member.name
			: member.name_en || member.name;
	};

	console.log("Data:", data);
	// console.log("Error:", error);
	// console.log("Is loading:", isLoading);

	if (isLoading) return <p>Loading...</p>;
	if (error) return <p>Error loading team members</p>;

	return (
		<div>
			<h2>{t("our_team")}</h2>
			<div>
				{teamData.length > 0 ? (
					teamData.map((member, index) => (
						<div key={member.id || index}>
							<img
								src={member.photo_thumbnail_url}
								alt={getTranslatedName(member)}
							/>
							<p>{getTranslatedName(member)}</p>
							{member.surname && <p>{member.surname}</p>}
							{member.mobile && <p>{member.mobile}</p>}
							{member.linkedin && (
								<a
									href={member.linkedin}
									target="_blank"
									rel="noopener noreferrer"
								>
									LinkedIn
								</a>
							)}
						</div>
					))
				) : (
					<p>No team members</p>
				)}
			</div>
		</div>
	);
};
