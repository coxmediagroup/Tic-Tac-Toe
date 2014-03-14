function table(app_parent) {
			var self 	= this;
			
			/*
				the information stored in grids is used to render the 
				spatial layout of all the grids in the table
			*/
			self.grids	= [];

			//---------------------creates grids in table
			self.grids.push( new grid(0,0,0, app_parent) );
			self.grids.push( new grid(1,0,1, app_parent) );
			self.grids.push( new grid(2,0,2, app_parent) );
			
			self.grids.push( new grid(0,1,3, app_parent) );
			self.grids.push( new grid(1,1,4, app_parent) );
			self.grids.push( new grid(2,1,5, app_parent) );
			
			self.grids.push( new grid(0,2,6, app_parent) );
			self.grids.push( new grid(1,2,7, app_parent) );
			self.grids.push( new grid(2,2,8, app_parent) );			
			//---------------------creates grids in table	
		}