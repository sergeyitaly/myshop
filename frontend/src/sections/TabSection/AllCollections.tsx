import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { useGetAllCollectionsQuery } from "../../api/collectionSlice";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { allCollectionSettings } from "./sliderSettings/AllCollectionSetting";
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../../constants";
import { useTranslation } from "react-i18next";

export const AllCollections = () => {
	const navigate = useNavigate();

	const { i18n } = useTranslation();
	const language = i18n.language;

	const { data, isLoading } = useGetAllCollectionsQuery();

	const collections = data?.results || [];

	const getTranslatedCollectionName = (
		collection: any,
		language: string
	): string => {
		return language === "uk"
			? collection.name_uk || collection.name
			: collection.name_en || collection.name;
	};

	const getTranslatedCategoryName = (
		category: any,
		language: string
	): string => {
		return language === "uk"
			? category?.name_uk || category?.name
			: category?.name_en || category?.name;
	};

	return (
		<AppSlider isLoading={isLoading} sliderSettings={allCollectionSettings}>
			{collections.map((collection) => {
				const { id, photo, photo_thumbnail_url, category } = collection;
				const translatedName = getTranslatedCollectionName(
					collection,
					language
				);

				const translatedCategory = getTranslatedCategoryName(
					category,
					language
				);

				return (
					<PreviewCard
						key={id}
						photoSrc={photo}
						previewSrc={photo_thumbnail_url}
						subTitle={translatedCategory}
						title={translatedName}
						onClick={() => navigate(`${ROUTE.COLLECTION}${id}`)}
					/>
				);
			})}
		</AppSlider>
	);
};
