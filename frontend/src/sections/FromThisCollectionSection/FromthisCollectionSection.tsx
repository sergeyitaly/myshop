// import { skipToken } from "@reduxjs/toolkit/query";
// import { useGetAllProductsFromCollectionQuery } from "../../api/collectionSlice";
// import { NamedSection } from "../../components/NamedSection/NamedSection";
// import { useAppTranslator } from "../../hooks/useAppTranslator";
// import { AppSlider } from "../../components/AppSlider/AppSlider";
// import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
// import { Product } from "../../models/entities";
// import { ROUTE } from "../../constants";
// import { useNavigate } from "react-router-dom";

//   interface FromThisCollectionProps {
//     collectionId?: number
//   }

// export const FromThisCollectionSection = ({collectionId}: FromThisCollectionProps) => {

//     const navigate = useNavigate()

//     const { data, isLoading } = useGetAllProductsFromCollectionQuery(collectionId ?? skipToken);

//     const {t, getTranslatedProductName} = useAppTranslator()

//     const handleClickSlide = (productItem: Product) => {
//       navigate(`${ROUTE.PRODUCT}${productItem.id}`);
//   }

//   const products = data?.results || []
//   console.log(products);

//     return (
//       <NamedSection
//       title={t('also_from_this_collection')}
//   >
//           <AppSlider
//               isLoading = {isLoading}
//           >
//               {products.map((product) => (
//                       <PreviewCard
//                           key={product.id}
//                           title={getTranslatedProductName(product)}  // Use translated name or fallback
//                           discount={product.discount}
//                           price={product.price}
//                           currency={product.currency}
//                           photoSrc={product.photo_url || ''}
//                           previewSrc={product.photo_thumbnail_url || ''}
//                           onClick={() => handleClickSlide(product)}
//                       />
//               ))}
//           </AppSlider>
//   </NamedSection>
//     )
// }

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { skipToken } from "@reduxjs/toolkit/query";
import { useGetProductsFromCollectionByProductFilterQuery } from "../../api/collectionSlice";
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { Pagination } from "../../components/UI/Pagination/Pagination";
import { useAppTranslator } from "../../hooks/useAppTranslator";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { Product } from "../../models/entities";
import { ROUTE } from "../../constants";

interface FromThisCollectionProps {
	collectionId?: number;
}

export const FromThisCollectionSection = ({
	collectionId,
}: FromThisCollectionProps) => {
	const LIMIT = 4;
	const navigate = useNavigate();
	const [currentPage, setCurrentPage] = useState<number>(1);
	const [totalPages, setTotalPages] = useState(0);
	const { t, getTranslatedProductName } = useAppTranslator();

	const { data, isLoading } =
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

	const handleClickSlide = (productItem: Product) => {
		navigate(`${ROUTE.PRODUCT}${productItem.id}`);
	};

	const handlePageChange = (page: number) => {
		setCurrentPage(page);
	};

	return (
		<NamedSection title={t("also_from_this_collection")}>
			<AppSlider isLoading={isLoading}>
				{products.map((product) => (
					<PreviewCard
						key={product.id}
						title={getTranslatedProductName(product)}
						discount={product.discount}
						price={product.price}
						currency={product.currency}
						photoSrc={product.photo_url || ""}
						previewSrc={product.photo_thumbnail_url || ""}
						onClick={() => handleClickSlide(product)}
					/>
				))}
			</AppSlider>

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
