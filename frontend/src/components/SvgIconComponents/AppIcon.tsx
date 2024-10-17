import { SVGProps } from "react"
import { CartIcon } from "./CartIcon"
import { CrossSign } from "./CrossSign"
import { VaseIcon } from "./VaseIcon"
import DeleteIcon from '@mui/icons-material/Delete';
import { AppIconNames } from "../../constants";
import { SearchIcon } from "./SearchIcon";
import { LeftArrowIcon } from "./LeftArrowIcon";
import { RightArrowIcon } from "./RightArrowIcon";
import { ForwardArrowIcon } from "./ForwardArrow";
import { UkraineFlagIcon } from "./UkraineFlag";
import { UKFlagIcon } from "./UKFlagIcon";
import { Face1 } from "./Face1";
import { Face2 } from "./Face2";
import { Face3 } from "./Face3";
import { Face4 } from "./Face4";

interface AppIconProps extends SVGProps<SVGSVGElement> {
    iconName: AppIconNames
}

export const AppIcon = ({iconName, ...props}: AppIconProps) => {
    
    switch (iconName){
        case 'cart': return <CartIcon {...props}/>
        case 'cross': return <CrossSign {...props}/>
        case 'vase': return <VaseIcon {...props}/>
        case 'delete': return <DeleteIcon />
        case 'search': return <SearchIcon {...props}/>
        case 'leftArrow': return <LeftArrowIcon {...props}/>
        case 'rigrtArrow': return <RightArrowIcon {...props}/>
        case 'forwardArrow': return <ForwardArrowIcon {...props}/>
        case 'flagUkraine' : return <UkraineFlagIcon {...props}/>
        case 'flagUK' : return <UKFlagIcon {...props}/>
        case 'face1' : return <Face1 {...props}/>
        case 'face2' : return <Face2 {...props}/>
        case 'face3' : return <Face3 {...props}/>
        case 'face4' : return <Face4 {...props}/>
        default: return <CartIcon {...props}/>
    }
}