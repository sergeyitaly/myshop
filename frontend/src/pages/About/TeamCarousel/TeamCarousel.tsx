import React from "react";
import { useGetTeamMembersQuery } from "../../../api/aboutSlice";
import { AppSlider } from "../../../components/AppSlider/AppSlider";
import { TeamItem } from "./TeamItem";
import { teamSettings } from "./teamSettings";
import { useTranslation } from "react-i18next";
import styles from "./TeamCarousel.module.scss";

export const TeamCarousel: React.FC = () => {
	const { t } = useTranslation();

	const { data, isError, isLoading } = useGetTeamMembersQuery();
	const teamData = data?.results || [];

	return (
		<div className={styles.container}>
			<div className={styles.title}>{t("our_team")}</div>
			{isError ? (
				<p>{t("empty_team")}</p>
			) : (
				<div className={styles.sliderContainer}>
					<AppSlider
						isLoading={isLoading}
						sliderSettings={teamSettings}
					>
						{teamData.map((member, index) => (
							<TeamItem key={index} member={member} />
						))}
					</AppSlider>
				</div>
			)}
		</div>
	);
};
