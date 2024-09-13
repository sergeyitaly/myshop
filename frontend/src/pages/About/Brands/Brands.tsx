import React from "react";
import { useGetBrandsQuery } from "../../../api/aboutSlice";
import { useTranslation } from "react-i18next";
import { BrandItem } from "./BrandsItem";
import { Skeleton } from "../../../components/Skeleton/Skeleton";
import styles from "./Brands.module.scss";

export const Brands: React.FC = () => {
	const { data, isError, isLoading } = useGetBrandsQuery();
	const { t } = useTranslation();
	const brandData = data?.results || [];

	return (
		<div className={styles.container}>
			<div className={styles.title}>{t("brands")}</div>
			<div className={styles.content}>
				{isLoading ? (
					Array.from({ length: 4 }).map((_, index) => (
						<div key={index} className={styles.skeletonWrapper}>
							<Skeleton className={styles.imageSkeleton} />
						</div>
					))
				) : isError ? (
					<p>{t("products.error")}</p>
				) : brandData.length > 0 ? (
					brandData.map((brandItem, index) => (
						<BrandItem key={index} brand={brandItem} />
					))
				) : (
					<p>{t("empty_brands")}</p>
				)}
			</div>
		</div>
	);
};
