import LogoSVG from "./logo.svg";
import vaseSVG from "./img.svg";
import { Link } from "react-router-dom";
import clsx from "clsx";
import styles from "./Logo.module.scss";

interface LogoProps {
	className?: string;
	type?: "full" | "short";
}

export const Logo = ({ className, type = "full" }: LogoProps) => {
	return (
		<div className={clsx(styles.logo, className)}>
			<Link to={"/"}>
				<img
					className={styles.logo}
					src={type === "full" ? LogoSVG : vaseSVG}
					alt="Koloryt Logo"
				/>
			</Link>
		</div>
	);
};
