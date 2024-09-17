import React, { useCallback } from "react";
import { TeamMember } from "../../../models/entities";
import { AppImage } from "../../../components/AppImage/AppImage";
import { useTranslation } from "react-i18next";
import { LinkedIn, Telegram, Email } from "@mui/icons-material";
import styles from "../TeamCarousel/TeamCarousel.module.scss";

interface TeamMemberProps {
	member: TeamMember;
}

export const TeamItem: React.FC<TeamMemberProps> = ({ member }) => {
	const { i18n } = useTranslation();
	const language = i18n.language;

	const {
		name,
		name_uk,
		name_en,
		surname,
		surname_uk,
		surname_en,
		description,
		description_uk,
		description_en,
		photo_url,
		linkedin,
		link_to_telegram,
		email,
	} = member;

	const getTranslatedName = useCallback(() => {
		return language === "uk" ? name_uk || name : name_en || name;
	}, [language, name, name_uk, name_en]);

	const getTranslatedSurname = useCallback(() => {
		return language === "uk"
			? surname_uk || surname
			: surname_en || surname;
	}, [language, surname, surname_uk, surname_en]);

	const getTranslatedDescription = useCallback(() => {
		return language === "uk"
			? description_uk || description || ""
			: description_en || description || "";
	}, [language, description, description_uk, description_en]);

	const translatedName = getTranslatedName();
	const translatedSurname = getTranslatedSurname();
	const translatedDescription = getTranslatedDescription();

	return (
		<div className={styles.teamItem}>
			<AppImage
				src={photo_url}
				alt={translatedName}
				className={styles.imageSize}
			/>

			<p className={styles.name}>
				{translatedName} {translatedSurname}
			</p>

			<p className={styles.description}>{translatedDescription}</p>

			<div className={styles.links}>
				{linkedin && (
					<a
						href={linkedin}
						target="_blank"
						rel="noopener noreferrer"
					>
						<LinkedIn />
					</a>
				)}
				{link_to_telegram && (
					<a
						href={link_to_telegram}
						target="_blank"
						rel="noopener noreferrer"
					>
						<Telegram />
					</a>
				)}
				{email && (
					<a href={`mailto:${email}`}>
						<Email />
					</a>
				)}
			</div>
		</div>
	);
};
