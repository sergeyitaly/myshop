import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { skipToken } from "@reduxjs/toolkit/query";
import { useGetProductsFromCollectionByProductFilterQuery } from "../../api/collectionSlice";
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { Pagination } from "../../components/UI/Pagination/Pagination";
import { useAppTranslator } from "../../hooks/useAppTranslator";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { ROUTE } from "../../constants";
import { PreviewLoadingCard } from "../../components/Cards/PreviewCard/PreviewLoagingCard";
import { MapComponent } from "../../components/MapComponent";
import styles from "./FromthisCollectionSection.module.scss";

interface FromThisCollectionProps {
	collectionId?: number;
}

export const FromThisCollectionSection = ({
	collectionId,
}: FromThisCollectionProps) => {
	const LIMIT = 4;
	const [currentPage, setCurrentPage] = useState<number>(1);
	const [totalPages, setTotalPages] = useState(0);
	const { t, getTranslatedProductName } = useAppTranslator();

	const { data, isLoading, isFetching } =
		useGetProductsFromCollectionByProductFilterQuery(
			collectionId !== undefined
				? {
						collectionId: collectionId,
						page: currentPage,
						page_size: LIMIT,
					}
				: skipToken
		);

	const products = data?.results || [];

	useEffect(() => {
		if (data) {
			const count = data.count;
			setTotalPages(Math.ceil(count / LIMIT));
		}
	}, [data]);

	const handlePageChange = (page: number) => {
		setCurrentPage(page);
	};

	return (
		<NamedSection title={t("also_from_this_collection")}>
			<div className={styles.wrapper}>
				{isLoading || isFetching ? (
					<MapComponent component={<PreviewLoadingCard />} qty={4} />
				) : (
					products.map((product) => (
						<Link
							key={product.id}
							to={`${ROUTE.PRODUCT}${product.id_name}`}
							rel="noopener noreferrer"
						>
							<PreviewCard
								key={product.id}
								title={getTranslatedProductName(product)}
								discount={product.discount}
								price={product.price}
								currency={product.currency}
								photoSrc={product.photo_url || ""}
								previewSrc={product.photo_thumbnail_url || ""}
							/>{" "}
						</Link>
					))
				)}
			</div>

			{data?.count && totalPages > 1 && (
				<Pagination
					totalPages={totalPages}
					currentPage={currentPage}
					onChange={handlePageChange}
				/>
			)}
		</NamedSection>
	);
};
