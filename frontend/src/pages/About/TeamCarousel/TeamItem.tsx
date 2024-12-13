import { TeamMember } from "../../../models/entities";
import { AppImage } from "../../../components/AppImage/AppImage";
import { useTranslation } from "react-i18next";
import { LinkedIn, Telegram, GitHub, Email } from "@mui/icons-material";
import { FaBehance } from "react-icons/fa";
import { getTranslatedText } from "../translation";
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
		role,
		role_en,
		role_uk,
		experience,
		experience_en,
		experience_uk,
		description,
		description_uk,
		description_en,
		photo_url,
		linkedin,
		link_to_telegram,
		github,
		behance,
		email,
	} = member;

	const translatedName = getTranslatedText(name, name_uk, name_en, language);
	const translatedSurname = getTranslatedText(
		surname,
		surname_uk,
		surname_en,
		language
	);

	const translatedRole = getTranslatedText(role, role_uk, role_en, language);
	const translatedExperience = getTranslatedText(
		experience,
		experience_uk,
		experience_en,
		language
	);
	const translatedDescription = getTranslatedText(
		description,
		description_uk,
		description_en,
		language
	);

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

			<p className={styles.role}>{translatedRole}</p>

			<p className={styles.experience}>{translatedExperience}</p>

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
				{github && (
					<a href={github} target="_blank" rel="noopener noreferrer">
						<GitHub />
					</a>
				)}
				{behance && (
					<a href={behance} target="_blank" rel="noopener noreferrer">
						<FaBehance />
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
