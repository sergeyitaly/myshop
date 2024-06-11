import { useEffect, useState } from 'react'
import { Product, ProductVariantsModel } from '../../models/entities'
import { PageContainer } from '../PageContainer'
import { DropDown } from './components/DropDown/DropDown'
import { ProductControl } from './components/ProductControl/ProductControl'
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import { Modal, useMediaQuery } from '@mui/material'
import Slider from 'react-slick'
import { settings } from './SliderSettings'
import style from './ProductInfoSection.module.scss'
import { screens } from '../../constants'



interface ProductInfoSectionProps {
    product: Product
    productVariants: ProductVariantsModel
    onChangeColor?: (color: string) => void
    onChangeSize?: (size: string) => void
}

export const ProductInfoSection = ({
    product,
    productVariants,
    onChangeColor,
    onChangeSize
}: ProductInfoSectionProps) => {

    
    const [currentImage, setCurrentImage] = useState<string>(product.photo)
    const [bigImage, setBigImage] = useState<string | null>(null)

    const isMobile = useMediaQuery(screens.maxMobile)

    console.log(isMobile);
    

    useEffect(() => {
        setCurrentImage(product.photo)
    }, [product.photo])
  

    const openModal = () => {
        setBigImage(currentImage)
    }

    const closeModal = () => {
        setBigImage(null)
    }

    return (
    <>
        <section >
            <PageContainer className={style.container}>
                {
                    isMobile ?
                    <Slider {...settings} className={style.imageBox}>
                        {
                            product.images?.map((image) => (
                            <div 
                                key={image.id}
                                className={style.slide}
                            >
                                <img src={image.images}/>
                                <button 
                                className={style.zoomButton}
                                onClick={openModal}
                                >
                                    <ZoomInIcon/>
                                </button>
                            </div>
                            ))
                        }
                    </Slider>
                    :
                    <>
                        <div className={style.wrapper}>
                            <div className={style.imageList}>
                                {
                                    product.images?.map((image) => (
                                    <div 
                                        key={image.id}
                                        className={style.previevBox}
                                        onClick={() => setCurrentImage(image.images)}
                                    >
                                        <img src={image.images}/>
                                    </div>
                                    ))
                                }
                            </div>
                        </div>
                        <div 
                            className={style.imageBox}
                            onClick={openModal}    
                        >
                            <img 
                                className={style.image}
                                src={currentImage}
                            />
                        </div>
                    </>
                }
            
                <div className={style.productInfo}>
                    <ProductControl 
                        product={product}
                        variants={productVariants}
                        onChangeColor={onChangeColor}
                        onChangeSize={onChangeSize}
                    />
                    <div className={style.description}>
                        <h3>Опис:</h3>
                        <p>{product.description ? product.description : 'опис товару поки що відсутній'}</p>
                    </div>
                </div>

                <DropDown
                    className={style.applyDropdown}
                    title='Застосування:'
                    content='Підходить для повсякденного носіння, а також стане чудовим доповненням до вечірнього або урочистого вбрання.'
                />
                <DropDown
                    className={style.careDropdown}
                    title='Догляд:'
                    content="Чистка: Використовуйте м'яку тканину або спеціалізований розчин для чищення срібла. Не використовуйте абразивні засоби, оскільки вони можуть пошкодити покриття.

                    Зберігання: Зберігайте кольє окремо від інших ювелірних виробів, щоб уникнути подряпин. Використовуйте м'яку тканинну сумочку або коробку з м'яким покриттям.
                    Уникайте контакту з хімікатами: Не допускайте контакту кольє з парфумами, косметикою, миючими засобами та іншими хімікатами, які можуть пошкодити позолоту.

                    Носіння: Намагайтеся надягати кольє після того, як ви нанесли косметику та парфуми, та знімати перед купанням, спортом або сном.
                    Дотримуючись цих рекомендацій, ви зможете довше зберігати красу та блиск вашого кольє з срібла з позолотою."
                />
            </PageContainer>
        </section>
        <Modal
            open={!!bigImage}
            className={style.center}
        >
            {
                bigImage ?
                <div 
                    className={style.zoomImage}
                    onClick={closeModal}
                >
                    <img src={bigImage} />
                </div>
                :
                <div>No image</div>
            }
        </Modal>
    </>
    )
}