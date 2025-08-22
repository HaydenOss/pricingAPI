// import SelectionUI from "@/components/store-selection";
import StoreList from "@/components/store-list"

export default function Home() {


  return (
    <div className="flex flex-row">

      <div className="bg-white border-5 border-blue w-1/3 h-100">
        <h1 className="text-black">Stores</h1>
        <StoreList />
        {/* <SelectionUI /> */}
      </div>
      <div>
        {/* Interactive Map */}
      </div>
      <div>
        {/* Shopping List */}
      </div>
    </div>
  );
}
