import React from "react";
import { useGetBrandsQuery } from "../../../api/aboutSlice";
import { Brand } from "../../../models/entities";
import { useTranslation } from "react-i18next";

export const Brands: React.FC = () => {
	const { data, error, isLoading } = useGetBrandsQuery();
	const { t, i18n } = useTranslation();
	const language = i18n.language;

	const brandData = data?.results || [];

	const getTranslatedName = (brandItem: Brand): string => {
		return language === "uk"
			? brandItem.name_uk || brandItem.name
			: brandItem.name_en || brandItem.name;
	};

	console.log("Data:", data);
	// console.log("Error:", error);
	// console.log("Is loading:", isLoading);

	if (isLoading) return <p>Loading...</p>;
	if (error) return <p>Error loading brands</p>;

	return (
		<div>
			<h2>{t("brands")}</h2>
			<div>
				{brandData.length > 0 ? (
					brandData.map((brandItem, index) => (
						<div key={brandItem.id || index}>
							<img
								src={brandItem.photo_thumbnail_url}
								alt={getTranslatedName(brandItem)}
							/>
							<p>{getTranslatedName(brandItem)}</p>

							{brandItem.link && (
								<a
									href={brandItem.link}
									target="_blank"
									rel="noopener noreferrer"
								>
									{brandItem.link}
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
